import random
from typing import Dict

from typing import List, Dict, Any, Union
from django.contrib.auth.models import User
from casino_main.models import Profile


class Card:
    """Refactoring Technique: Replace Conditional with Polymorphism"""
    FACE_CARD_VALUES = {'J': 10, 'Q': 10, 'K': 10}

    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit

    def get_value(self) -> int:
        """Refactoring Technique: Extract Method"""
        if self.rank == 'A':
            return 11
        return self.FACE_CARD_VALUES.get(self.rank, int(self.rank))

    def to_dict(self) -> Dict[str, str]:
        """Refactoring Technique: Tell, Don't Ask"""
        return {'rank': self.rank, 'suit': self.suit}


class BlackjackGame:
    """Refactoring Technique: Extract Class (separating responsibilities)"""
    def __init__(self):
        self.player_hand: List[Card] = []
        self.dealer_hand: List[Card] = []
        self.deck: List[Card] = []
        self.game_over: bool = False

    @classmethod
    def create_deck(cls) -> List[Card]:
        """Refactoring Technique: Replace Method with Method Object"""
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['♠', '♥', '♣', '♦']
        deck = [Card(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def deal_card(self) -> Card:
        """Refactoring Technique: Introduce Guard Clause"""
        if not self.deck:
            self.deck = self.create_deck()
        return self.deck.pop()

    def card_value(self, card):
        return card.get_value()

    def _handle_aces(self, total, aces):
        """Extract Method"""

        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def calculate_hand(self, hand: List[Card]) -> int:
        """Refactoring Technique: Replace Temp with Query"""
        total = sum(card.get_value() for card in hand)
        aces = sum(1 for card in hand if card.rank == 'A')
        return self._handle_aces(total, aces)

    def start_game(self):
        self.create_deck()
        self.player_hand = [self.deal_card(), self.deal_card()]
        self.dealer_hand = [self.deal_card(), self.deal_card()]
        self.game_over = False

    def player_hit(self):
        self.player_hand.append(self.deal_card())
        player_score = self.calculate_hand(self.player_hand)

        if player_score > 21:
            self.game_over = True
            return "Bust! You lose."
        elif player_score == 21:
            return "Blackjack! 21 points."
        return None

    def dealer_play(self):

        while self.calculate_hand(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deal_card())

        player_score = self.calculate_hand(self.player_hand)
        dealer_score = self.calculate_hand(self.dealer_hand)

        self.game_over = True


        if dealer_score > 21:
            return "Dealer busts! You win!"
        elif dealer_score == player_score:
            return "It's a tie!"
        elif dealer_score > player_score:
            return "Dealer wins!"
        else:
            return "You win!"

    def get_game_state(self) -> Dict[str, Any]:
        """Refactoring Technique: Rename Method (more descriptive)"""
        dealer_score = (self.card_value(self.dealer_hand[0])
                        if not self.game_over and self.dealer_hand
                        else self.calculate_hand(self.dealer_hand))

        return {
            'player_hand': [card.to_dict() for card in self.player_hand],
            'dealer_hand': [card.to_dict() for card in self.dealer_hand],
            'player_score': self.calculate_hand(self.player_hand),
            'dealer_score': dealer_score,
            'game_over': self.game_over,
        }

    def card_value(self, card: Card) -> int:
        """Refactoring Technique: Remove Middle Man"""
        return card.get_value()