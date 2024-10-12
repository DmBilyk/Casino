from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from casino_main.models import Profile
from .game_logic import BlackjackGame, Card
import json


@login_required
def game(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

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
        'balance': profile.balance,
        'bet': request.session.get('bet', 0),
    }
    return render(request, 'blackjack_app/game.html', context)


@login_required
def start_game(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    game = BlackjackGame()
    game_state = request.session['game']
    game.dealer_hand = [Card(**card) for card in game_state['dealer_hand']]
    game.dealer_hand.append(game.deal_card())  # Deal the second card to the dealer
    game.player_hand = [game.deal_card(), game.deal_card()]  # Deal two cards to the player
    request.session['game'] = game.get_game_state()

    return JsonResponse({
        'game_state': request.session['game'],
        'balance': profile.balance,
        'bet': request.session.get('bet', 0),
    })


@login_required
def hit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    game = BlackjackGame()
    game_state = request.session['game']
    game.player_hand = [Card(**card) for card in game_state['player_hand']]
    game.dealer_hand = [Card(**card) for card in game_state['dealer_hand']]
    game.game_over = game_state['game_over']

    result = game.player_hit()
    request.session['game'] = game.get_game_state()

    if result == "Bust! You lose.":
        bet = request.session.get('bet', 0)
        profile.balance -= bet
        profile.save()
        request.session['bet'] = 0

    return JsonResponse({
        'game_state': request.session['game'],
        'balance': profile.balance,
        'bet': request.session.get('bet', 0),
        'message': result,
    })


@login_required
def stay(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    game = BlackjackGame()
    game_state = request.session['game']
    game.player_hand = [Card(**card) for card in game_state['player_hand']]
    game.dealer_hand = [Card(**card) for card in game_state['dealer_hand']]

    result = game.dealer_play()
    request.session['game'] = game.get_game_state()

    bet = request.session.get('bet', 0)
    if "You win" in result:
        profile.balance += bet * 2
    elif "Dealer wins" in result:
        profile.balance -= bet
    else:  # It's a tie
        pass  # The bet is returned to the player

    profile.save()
    request.session['bet'] = 0

    return JsonResponse({
        'game_state': request.session['game'],
        'balance': profile.balance,
        'bet': request.session['bet'],
        'message': result,
    })


@login_required
def place_bet(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    amount = int(request.GET.get('amount', 0))
    current_bet = request.session.get('bet', 0)

    if amount == 0:
        profile.balance += current_bet
        request.session['bet'] = 0
    elif profile.balance >= amount:
        request.session['bet'] = request.session.get('bet', 0) + amount

    profile.save()

    return JsonResponse({
        'balance': profile.balance,
        'bet': request.session['bet'],
        'game_state': request.session['game'],
    })