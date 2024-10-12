from django.shortcuts import render
from django.http import JsonResponse
import random
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from casino_main.models import Profile


def initialize_session(request):
    if 'first_visit' not in request.session:
        request.session['first_visit'] = True



@login_required
def slot_machine(request):

    profile, created = Profile.objects.get_or_create(user=request.user)
    context = {
        'balance': profile.balance,
    }
    return render(request, 'slot_machine_app/slot_machine.html', context)

@login_required
def spin(request):
    initialize_session(request)

    profile, created = Profile.objects.get_or_create(user=request.user)
    if profile.balance < 25:
        return JsonResponse({'error': 'Insufficient balance'}, status=400)

    profile.balance -= 25

    symbols = ['🍋', '🍒', '7️⃣', '💎', '🍀','🍒','🍀']

    is_first_visit = request.session.get('first_visit', True)
    if is_first_visit:
        result = ['💎', '💎', '💎']
        request.session['first_visit'] = False
        request.session.modified = True
    else:
        result = [random.choice(symbols) for _ in range(3)]

    win_amount = calculate_win(result)
    profile.balance += win_amount
    profile.save()

    return JsonResponse({
        'result': result,
        'balance': profile.balance,
        'win_amount': win_amount,
    })

def calculate_win(result):
    if len(set(result)) == 1:
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
        if result[0] == '💎' and result[2] == '💎':
            return 100
        elif result[0] == '7️⃣' and result[1] == '7️⃣':
            return 50
    elif len(set(result)) == 3:
        if result[0] == '🍋' or result[1] == '🍋' or result[2] == '🍋':
            return 25

    return 0