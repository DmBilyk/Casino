from django.urls import path, include
from .views import GameStateView, DealCardsView, HitView, StayView, BetView, game_template_view, GoogleAuthTokenView, NewGameView

app_name = 'blackjack_app'

urlpatterns = [
    # URL pattern for rendering the game template view
    path('game/', game_template_view, name='game'),

    # URL pattern for getting the current game state
    path('api/game/state/', GameStateView.as_view(), name='game-state'),

    # URL pattern for dealing initial cards to start the game
    path('api/game/deal/', DealCardsView.as_view(), name='deal-cards'),

    # URL pattern for handling player taking another card
    path('api/game/hit/', HitView.as_view(), name='hit'),

    # URL pattern for handling player standing with current cards
    path('api/game/stay/', StayView.as_view(), name='stay'),

    # URL pattern for placing a bet
    path('api/game/bet/', BetView.as_view(), name='bet'),

    # URL pattern for starting a new game
    path('api/game/new/', NewGameView.as_view(), name='new-game'),
]