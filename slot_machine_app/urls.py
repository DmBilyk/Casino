from django.urls import path
from . import views

urlpatterns = [
    path('', views.slot_machine, name='slot_machine'),
    path('spin/', views.spin, name='spin'),
]