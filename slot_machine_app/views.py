from django.shortcuts import render
from django.http import JsonResponse
import random


def initialize_session(request):
    if 'balance' not in request.session:
        request.session['balance'] = 1000


def slot_machine(request):
    initialize_session(request)
    context = {
        'balance': request.session['balance'],
    }
    return render(request, 'slot_machine_app/slot_machine.html', context)


def spin(request):
    initialize_session(request)

    if request.session['balance'] < 10:
        return JsonResponse({'error': 'Insufficient balance'}, status=400)

    request.session['balance'] -= 10

    symbols = ['🍋', '🍒', '7️⃣', '💎', '🍀']
    result = [random.choice(symbols) for _ in range(3)]

    win_amount = calculate_win(result)
    request.session['balance'] += win_amount

    return JsonResponse({
        'result': result,
        'balance': request.session['balance'],
        'win_amount': win_amount,
    })


def calculate_win(result):
    if len(set(result)) == 1:  # All symbols are the same
        if result[0] == '🍋':
            return 1000
        elif result[0] == '🍒':
            return 50
        elif result[0] == '7️⃣':
            return 500
        elif result[0] == '💎':
            return 750
        elif result[0] == '🍀':
            return 250
    elif len(set(result)) == 2:
        if result[0] == '💎' and result[1] == '💎' or result[0] == '💎' and result[2] == '💎' or result[1] == '💎' and result[2] == '💎':
            return 100
        elif result[0] == '7️⃣' and result[1] == '7️⃣' or result[0] == '7️⃣' and result[2] == '7️⃣' or result[1] == '7️⃣' and result[2] == '7️⃣':
            return 50
    elif len(set(result)) == 3:
        if result[0] == '🍋' or result[1] == '🍋' or result[2] == '🍋':
            return 10

    return 0