document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const messageArea = document.getElementById('messageArea');
    const dealerCards = document.getElementById('dealerCards');
    const playerCards = document.getElementById('playerCards');
    const playerScore = document.getElementById('playerScore');
    const dealerScore = document.getElementById('dealerScore');
    const playerBalance = document.getElementById('playerBalance');
    const currentBet = document.getElementById('currentBet');

    const hitBtn = document.getElementById('hitBtn');
    const stayBtn = document.getElementById('stayBtn');
    const startGameBtn = document.getElementById('startGameBtn');
    const clearBetBtn = document.getElementById('clearBetBtn');
    const chips = document.querySelectorAll('.chip');

    // Parse initial game state from the template
    let gameState = {
        player_hand: [],
        dealer_hand: [],
        player_score: 0,
        dealer_score: 0,
        game_over: true
    };

    // Try to extract initial game state from DOM
    try {
        // Get player cards
        const playerCardElements = document.querySelectorAll('#playerCards .card');
        if (playerCardElements.length > 0) {
            gameState.player_hand = Array.from(playerCardElements).map(card => {
                if (card.classList.contains('hidden-card')) return null;
                const rank = card.querySelector('.card-value').textContent;
                const suit = card.querySelector('.card-suit').textContent;
                return { rank, suit };
            }).filter(card => card !== null);
        }

        // Get dealer cards
        const dealerCardElements = document.querySelectorAll('#dealerCards .card');
        if (dealerCardElements.length > 0) {
            gameState.dealer_hand = Array.from(dealerCardElements).map(card => {
                if (card.classList.contains('hidden-card')) return null;
                const rank = card.querySelector('.card-value')?.textContent;
                const suit = card.querySelector('.card-suit')?.textContent;
                return rank && suit ? { rank, suit } : null;
            }).filter(card => card !== null);
        }

        // Parse scores from DOM
        const playerScoreText = playerScore.textContent;
        const dealerScoreText = dealerScore.textContent;
        gameState.player_score = parseInt(playerScoreText.replace('Score: ', '')) || 0;
        gameState.dealer_score = parseInt(dealerScoreText.replace('Score: ', '')) || 0;

        // Parse message to determine game state
        const messageText = messageArea.textContent.trim();
        gameState.game_over = messageText.includes('Game over') ||
                              messageText.includes('Start a new') ||
                              messageText.includes('Place your bet');
    } catch (e) {
        console.error('Error parsing initial game state:', e);
        // Fallback to default state
    }

    // Parse current bet and balance
    const betText = currentBet.textContent.replace('$', '').trim();
    const balanceText = playerBalance.textContent.replace('$', '').trim();
    let bet = parseInt(betText) || 0;
    let balance = parseInt(balanceText) || 1000;

    // Determine if game is in progress
    let gameInProgress = gameState.player_hand.length > 0 && !gameState.game_over;

    // Utility functions
    function renderCard(card, isRed = false) {
        return `
            <div class="card ${isRed ? 'red' : ''}">
                <div class="card-top">
                    <span class="card-value">${card.rank}</span>
                    <span class="card-suit">${card.suit}</span>
                </div>
                <div class="card-center">${card.suit}</div>
                <div class="card-bottom">
                    <span class="card-value">${card.rank}</span>
                    <span class="card-suit">${card.suit}</span>
                </div>
            </div>
        `;
    }

    function renderHiddenCard() {
        return `
            <div class="card hidden-card">
                <!-- Hidden card -->
            </div>
        `;
    }

    function updateUI(data) {
        // Update scores and balance
        playerScore.textContent = `Score: ${data.game_state.player_score}`;
        playerBalance.textContent = `$ ${data.balance}`;
        currentBet.textContent = `$ ${data.bet}`;

        // Update dealer score based on game state
        if (data.game_state.game_over) {
            dealerScore.textContent = `Score: ${data.game_state.dealer_score}`;
        } else {
            // If game is ongoing, show only the visible score
            const visibleScore = data.game_state.dealer_hand.length > 0 ?
                cardValue(data.game_state.dealer_hand[0]) : 0;
            dealerScore.textContent = `Score: ${visibleScore}`;
        }

        // Clear card displays
        dealerCards.innerHTML = '';
        playerCards.innerHTML = '';

        // Render dealer cards
        data.game_state.dealer_hand.forEach((card, index) => {
            const isLastCard = index === data.game_state.dealer_hand.length - 1;
            const shouldHide = isLastCard && !data.game_state.game_over;

            if (shouldHide) {
                dealerCards.innerHTML += renderHiddenCard();
            } else {
                const isRed = card.suit === '♥' || card.suit === '♦';
                dealerCards.innerHTML += renderCard(card, isRed);
            }
        });

        // Render player cards
        data.game_state.player_hand.forEach(card => {
            const isRed = card.suit === '♥' || card.suit === '♦';
            playerCards.innerHTML += renderCard(card, isRed);
        });

        // Update button states
        const hasCards = data.game_state.player_hand.length > 0;
        const gameOver = data.game_state.game_over;
        const hasBet = data.bet > 0;

        hitBtn.disabled = !hasCards || gameOver || !hasBet;
        stayBtn.disabled = !hasCards || gameOver || !hasBet;
        startGameBtn.disabled = !hasBet || (hasCards && !gameOver);

        // Update chips clickability
        chips.forEach(chip => {
            chip.style.opacity = gameOver ? "1" : "0.5";
            chip.style.cursor = gameOver ? "pointer" : "not-allowed";
        });
        clearBetBtn.disabled = !gameOver || bet === 0;

        // Display message if provided
        if (data.message) {
            messageArea.textContent = data.message;
        } else if (gameOver) {
            messageArea.textContent = 'Game over! Place a bet to play again.';
        } else if (!hasCards) {
            messageArea.textContent = 'Place your bet and start the game.';
        } else {
            messageArea.textContent = 'Your move!';
        }

        // Update game state
        gameInProgress = hasCards && !gameOver;

        // Store the updated state
        gameState = data.game_state;
        bet = data.bet;
        balance = data.balance;
    }

    function cardValue(card) {
        if (['J', 'Q', 'K'].includes(card.rank)) {
            return 10;
        } else if (card.rank === 'A') {
            return 11; // Simplified for UI purposes
        } else {
            return parseInt(card.rank);
        }
    }

    // API functions
    async function placeBet(amount) {
        try {
            const response = await fetch(`/place_bet?amount=${amount}`);
            const data = await response.json();
            updateUI(data);
            return data;
        } catch (error) {
            console.error('Error placing bet:', error);
            messageArea.textContent = 'Connection error. Please try again.';
        }
    }

    async function startGame() {
        try {
            const response = await fetch('/start_game');
            const data = await response.json();
            updateUI(data);
            return data;
        } catch (error) {
            console.error('Error starting game:', error);
            messageArea.textContent = 'Connection error. Please try again.';
        }
    }

    async function hit() {
        try {
            const response = await fetch('/hit');
            const data = await response.json();
            updateUI(data);
            return data;
        } catch (error) {
            console.error('Error hitting:', error);
            messageArea.textContent = 'Connection error. Please try again.';
        }
    }

    async function stay() {
        try {
            const response = await fetch('/stay');
            const data = await response.json();
            updateUI(data);
            return data;
        } catch (error) {
            console.error('Error staying:', error);
            messageArea.textContent = 'Connection error. Please try again.';
        }
    }

    // Event Listeners
    chips.forEach(chip => {
        chip.addEventListener('click', function() {
            if (gameInProgress) return;

            const amount = parseInt(this.dataset.value);
            placeBet(amount);
        });
    });

    clearBetBtn.addEventListener('click', function() {
        if (gameInProgress) return;
        placeBet(0);
    });

    startGameBtn.addEventListener('click', function() {
        if (gameInProgress) return;
        startGame();
    });

    hitBtn.addEventListener('click', function() {
        if (!gameInProgress) return;
        hit();
    });

    stayBtn.addEventListener('click', function() {
        if (!gameInProgress) return;
        stay();
    });

    // Initialize UI based on the parsed state
    updateUI({
        game_state: gameState,
        bet: bet,
        balance: balance
    });
});