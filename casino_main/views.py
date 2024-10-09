from django.shortcuts import render

def initialize_session(request):
    if 'balance' not in request.session:
        request.session['balance'] = 1000

def game_selection(request):
    initialize_session(request)
    context = {
        'balance': request.session['balance'],
    }
    return render(request, 'casino_main/game_selection.html', context)