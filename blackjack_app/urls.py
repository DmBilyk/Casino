from django.urls import path
from . import views
from blackjack_app.admin_views import edit_session_balance

urlpatterns = [
    path('', views.game, name='game'),
    path('hit/', views.hit, name='hit'),
    path('stay/', views.stay, name='stay'),
    path('place_bet/', views.place_bet, name='place_bet'),
    path('admin/edit_session_balance/', edit_session_balance, name='edit_session_balance'),

]