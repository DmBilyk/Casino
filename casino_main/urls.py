from django.urls import path
from . import views
from django.urls import include
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.game_selection, name='game_selection'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('logout/', LogoutView.as_view(), name='logout'),

]