from django.shortcuts import render, redirect
from django.http import JsonResponse
from .game_logic import BlackjackGame, Card

def initialize_session(request):
    if 'balance' not in request.session:
        request.session['balance'] = 1000
    if 'bet' not in request.session:
        request.session['bet'] = 0
    if 'game' not in request.session:
        request.session['game'] = None

def game(request):
    initialize_session(request)

    if request.GET.get('new_game'):
        request.session['game'] = None
        request.session['bet'] = 0

    game_state = request.session.get('game')
    if not game_state:
        game = BlackjackGame()
        game.create_deck()
        game.dealer_hand = [game.deal_card()]  # Deal only one card to the dealer initially
        request.session['game'] = game.get_game_state()
    else:
        game = BlackjackGame()
        game.player_hand = [Card(**card) for card in game_state['player_hand']]
        game.dealer_hand = [Card(**card) for card in game_state['dealer_hand']]
        game.game_over = game_state['game_over']

    context = {
        'game_state': request.session['game'],
        'balance': request.session['balance'],
        'bet': request.session['bet'],
    }
    return render(request, 'blackjack_app/game.html', context)

def start_game(request):
    initialize_session(request)
    game = BlackjackGame()
    game_state = request.session['game']
    game.dealer_hand = [Card(**card) for card in game_state['dealer_hand']]
    game.dealer_hand.append(game.deal_card())  # Deal the second card to the dealer
    game.player_hand = [game.deal_card(), game.deal_card()]  # Deal two cards to the player
    request.session['game'] = game.get_game_state()

    return JsonResponse({
        'game_state': request.session['game'],
        'balance': request.session['balance'],
        'bet': request.session['bet'],
    })

def hit(request):
    initialize_session(request)
    game = BlackjackGame()
    game_state = request.session['game']
    game.player_hand = [Card(**card) for card in game_state['player_hand']]
    game.dealer_hand = [Card(**card) for card in game_state['dealer_hand']]
    game.game_over = game_state['game_over']

    result = game.player_hit()
    request.session['game'] = game.get_game_state()

    if result == "Bust! You lose.":
        request.session['bet'] = 0

    return JsonResponse({
        'game_state': request.session['game'],
        'balance': request.session['balance'],
        'bet': request.session['bet'],
        'message': result,
    })

def stay(request):
    initialize_session(request)
    game = BlackjackGame()
    game_state = request.session['game']
    game.player_hand = [Card(**card) for card in game_state['player_hand']]
    game.dealer_hand = [Card(**card) for card in game_state['dealer_hand']]

    result = game.dealer_play()
    request.session['game'] = game.get_game_state()

    if "You win" in result:
        request.session['balance'] += request.session['bet'] * 2
    elif "Dealer wins" in result:
        pass
    else:  # It's a tie
        request.session['balance'] += request.session['bet']

    request.session['bet'] = 0

    return JsonResponse({
        'game_state': request.session['game'],
        'balance': request.session['balance'],
        'bet': request.session['bet'],
        'message': result,
    })

def place_bet(request):
    initialize_session(request)
    amount = int(request.GET.get('amount', 0))
    current_bet = request.session['bet']
    balance = request.session['balance']

    if amount == 0:  # Cancel bet
        request.session['balance'] += current_bet
        request.session['bet'] = 0
    elif balance >= amount:
        request.session['balance'] -= amount
        request.session['bet'] += amount

    return JsonResponse({
        'balance': request.session['balance'],
        'bet': request.session['bet'],
        'game_state': request.session['game'],
    })