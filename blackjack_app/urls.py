from django.urls import path, include
from .views import GameStateView, DealCardsView, HitView, StayView, BetView, game_template_view, GoogleAuthTokenView, NewGameView

app_name = 'blackjack_app'


urlpatterns = [



    path('game/', game_template_view, name='game'),
    path('api/game/state/', GameStateView.as_view(), name='game-state'),
    path('api/game/deal/', DealCardsView.as_view(), name='deal-cards'),
    path('api/game/hit/', HitView.as_view(), name='hit'),
    path('api/game/stay/', StayView.as_view(), name='stay'),
    path('api/game/bet/', BetView.as_view(), name='bet'),
    path('api/game/new/', NewGameView.as_view(), name='new-game'),

    ]