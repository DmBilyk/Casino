from django.urls import path
from . import views
from .admin_views import edit_all_session_balances

app_name = 'blackjack_app'

urlpatterns = [
    path('', views.game, name='game'),
    path('hit/', views.hit, name='hit'),
    path('stay/', views.stay, name='stay'),
    path('place_bet/', views.place_bet, name='place_bet'),
    path('admin/edit_all_balances/', edit_all_session_balances, name='edit_all_session_balances'),
]