from rest_framework import serializers
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from social_django.utils import psa
from django.contrib.auth.models import User

class CardSerializer(serializers.Serializer):

    rank = serializers.CharField()
    suit = serializers.CharField()

class GameStateSerializer(serializers.Serializer):

    player_hand = CardSerializer(many=True)
    dealer_hand = CardSerializer(many=True)
    player_score = serializers.IntegerField()
    dealer_score = serializers.IntegerField()
    game_over = serializers.BooleanField()

class BetSerializer(serializers.Serializer):

    amount = serializers.IntegerField(required=True, min_value=0)













class GoogleAuthTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()

    def validate(self, data):
        access_token = data['access_token']
        user = self._get_user_from_google_token(access_token)
        if user:
            return {
                'user': user,
                'token': self._create_jwt_token(user)
            }
        raise serializers.ValidationError("Invalid Google token")

    def _get_user_from_google_token(self, access_token):

        user = User.objects.filter(social_auth__extra_data__contains={'access_token': access_token}).first()
        return user

    def _create_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
