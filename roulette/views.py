from django.shortcuts import render
from django.http import JsonResponse
import random
import json

def initialize_session(request):
    if 'balance' not in request.session:
        request.session['balance'] = 1000

def roulette(request):
    initialize_session(request)
    context = {
        'balance': request.session['balance'],
    }
    return render(request, 'roulette/roulette.html', context)

def spin(request):
    initialize_session(request)

    bets = json.loads(request.POST.get('bets', '[]'))
    total_bet_amount = sum(bet['amount'] for bet in bets)

    if request.session['balance'] < total_bet_amount:
        return JsonResponse({'error': 'Insufficient balance'}, status=400)

    request.session['balance'] -= total_bet_amount

    result = random.randint(0, 36)
    color = 'red' if result in [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36] else 'black' if result != 0 else 'green'
    is_even = result % 2 == 0 and result != 0

    win_amount = 0
    for bet in bets:
        if (bet['type'] == 'red' and color == 'red') or \
           (bet['type'] == 'black' and color == 'black') or \
           (bet['type'] == 'even' and is_even) or \
           (bet['type'] == 'odd' and not is_even):
            win_amount += bet['amount'] * 2
        elif bet['type'].startswith('number') and int(bet['type'].split()[1]) == result:
            win_amount += bet['amount'] * 35

    request.session['balance'] += win_amount

    return JsonResponse({
        'result': f"{result} {color}",
        'balance': request.session['balance'],
        'win_amount': win_amount,
    })