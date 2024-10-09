from django.urls import path
from . import views
from blackjack_app.admin_views import edit_session_balance

urlpatterns = [
    path('', views.game_selection, name='game_selection'),

]