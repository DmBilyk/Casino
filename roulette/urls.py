from django.urls import path
from . import views
from .views import roulette, spin as roulette_spin

urlpatterns = [
    path('', views.roulette, name='roulette'),
    path('spin/', views.spin, name='roulette_spin'),
]