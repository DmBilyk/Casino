from rest_framework import serializers
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from social_django.utils import psa
from django.contrib.auth.models import User

class CardSerializer(serializers.Serializer):
    """
    Serializer for a playing card.
    """
    rank = serializers.CharField()
    suit = serializers.CharField()

class GameStateSerializer(serializers.Serializer):
    """
    Serializer for the game state.
    """
    player_hand = CardSerializer(many=True)
    dealer_hand = CardSerializer(many=True)
    player_score = serializers.IntegerField()
    dealer_score = serializers.IntegerField()
    game_over = serializers.BooleanField()

class BetSerializer(serializers.Serializer):
    """
    Serializer for placing a bet.
    """
    amount = serializers.IntegerField(required=True, min_value=0)

class GoogleAuthTokenSerializer(serializers.Serializer):
    """
    Serializer for Google authentication token.
    """
    access_token = serializers.CharField()

    def validate(self, data):
        """
        Validate the provided Google access token.

        Args:
            data (dict): The data containing the access token.

        Returns:
            dict: The validated data with user and JWT token.

        Raises:
            serializers.ValidationError: If the Google token is invalid.
        """
        access_token = data['access_token']
        user = self._get_user_from_google_token(access_token)
        if user:
            return {
                'user': user,
                'token': self._create_jwt_token(user)
            }
        raise serializers.ValidationError("Invalid Google token")

    def _get_user_from_google_token(self, access_token):
        """
        Retrieve the user associated with the provided Google access token.

        Args:
            access_token (str): The Google access token.

        Returns:
            User: The user associated with the token, or None if not found.
        """
        user = User.objects.filter(social_auth__extra_data__contains={'access_token': access_token}).first()
        return user

    def _create_jwt_token(self, user):
        """
        Create a JWT token for the given user.

        Args:
            user (User): The user for whom to create the token.

        Returns:
            str: The created JWT token.
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)