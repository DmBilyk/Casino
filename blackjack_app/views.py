from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from .facade import BlackjackGameFacade
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import GoogleAuthTokenSerializer, BetSerializer


class GoogleAuthTokenView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=GoogleAuthTokenSerializer,
        responses={200: openapi.Response('Access token response', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ))},
        operation_description="Exchange Google token for JWT token"
    )
    def post(self, request):
        serializer = GoogleAuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'access_token': serializer.validated_data['token']})
        return Response(serializer.errors, status=400)


class GameStateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: openapi.Response('Game state response', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'game_state': openapi.Schema(type=openapi.TYPE_OBJECT),
                'balance': openapi.Schema(type=openapi.TYPE_INTEGER),
                'bet': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ))},
        operation_description="Get current game state"
    )
    def get(self, request):
        facade = BlackjackGameFacade(request.user)
        result = facade.get_game_state(request.session)
        return Response(result)


class DealCardsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: openapi.Response('Deal cards response', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'game_state': openapi.Schema(type=openapi.TYPE_OBJECT),
                'balance': openapi.Schema(type=openapi.TYPE_INTEGER),
                'bet': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ))},
        operation_description="Deal initial cards to start the game"
    )
    def post(self, request):
        facade = BlackjackGameFacade(request.user)
        result = facade.deal_cards(request.session)
        return Response(result)


class HitView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: openapi.Response('Hit response', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'game_state': openapi.Schema(type=openapi.TYPE_OBJECT),
                'balance': openapi.Schema(type=openapi.TYPE_INTEGER),
                'bet': openapi.Schema(type=openapi.TYPE_INTEGER),
                'message': openapi.Schema(type=openapi.TYPE_STRING, nullable=True)
            }
        ))},
        operation_description="Player takes another card"
    )
    def post(self, request):
        facade = BlackjackGameFacade(request.user)
        result = facade.player_hit(request.session)
        return Response(result)


class StayView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: openapi.Response('Stay response', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'game_state': openapi.Schema(type=openapi.TYPE_OBJECT),
                'balance': openapi.Schema(type=openapi.TYPE_INTEGER),
                'bet': openapi.Schema(type=openapi.TYPE_INTEGER),
                'message': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ))},
        operation_description="Player stands with current cards"
    )
    def post(self, request):
        facade = BlackjackGameFacade(request.user)
        result = facade.player_stay(request.session)
        return Response(result)


class BetView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=BetSerializer,
        responses={200: openapi.Response('Bet response', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'game_state': openapi.Schema(type=openapi.TYPE_OBJECT),
                'balance': openapi.Schema(type=openapi.TYPE_INTEGER),
                'bet': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ))},
        operation_description="Place a bet"
    )
    def post(self, request):
        amount = request.data.get('amount', 0)
        facade = BlackjackGameFacade(request.user)
        result = facade.place_bet(request.session, amount)
        return Response(result)



class NewGameView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: openapi.Response('New game response', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'game_state': openapi.Schema(type=openapi.TYPE_OBJECT),
                'balance': openapi.Schema(type=openapi.TYPE_INTEGER),
                'bet': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ))},
        operation_description="Start a new game"
    )
    def post(self, request):
        facade = BlackjackGameFacade(request.user)
        result = facade.start_new_game(request.session)
        return Response(result)


@login_required
def game_template_view(request):
    return render(request, 'blackjack_app/game.html')