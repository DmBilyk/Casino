from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile


@login_required
def game_selection(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if created:
        profile.balance = 1000
        profile.save()

    context = {
        'balance': profile.balance,
    }
    return render(request, 'casino_main/game_selection.html', context)