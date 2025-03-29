from django.db import models
import random


class Card:
    """
    Represents a playing card with a rank and suit.
    """

    def __init__(self, rank, suit):
        """
        Initializes a card with the given rank and suit.

        Args:
            rank (str): The rank of the card (e.g., '2', 'A').
            suit (str): The suit of the card (e.g., '♠', '♥').
        """
        self.rank = rank
        self.suit = suit

    def __str__(self):
        """
        Returns a string representation of the card.

        Returns:
            str: The card's rank and suit.
        """
        return f"{self.rank}{self.suit}"


class BlackjackGame(models.Model):
    """
    Represents a game of Blackjack.
    """
    player_hand = models.JSONField(default=list)
    dealer_hand = models.JSONField(default=list)
    deck = models.JSONField(default=list)
    game_over = models.BooleanField(default=False)

    def create_deck(self):
        """
        Creates and shuffles a deck of 52 playing cards.

        Returns:
            list: A shuffled deck of cards.
        """
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['♠', '♥', '♣', '♦']
        deck = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def deal_card(self):
        """
        Deals a card from the deck.

        Returns:
            dict: The dealt card.
        """
        return self.deck.pop()

    def card_value(self, card):
        """
        Calculates the value of a card.

        Args:
            card (dict): The card to calculate the value for.

        Returns:
            int: The value of the card.
        """
        if card['rank'] in ['J', 'Q', 'K']:
            return 10
        elif card['rank'] == 'A':
            return 11
        else:
            return int(card['rank'])

    def calculate_hand(self, hand):
        """
        Calculates the total value of a hand.

        Args:
            hand (list): The hand to calculate the value for.

        Returns:
            int: The total value of the hand.
        """
        total = sum(self.card_value(card) for card in hand)
        aces = sum(1 for card in hand if card['rank'] == 'A')
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def start_game(self):
        """
        Starts a new game by dealing initial cards to the player and dealer.
        """
        self.deck = self.create_deck()
        self.player_hand = [self.deal_card(), self.deal_card()]
        self.dealer_hand = [self.deal_card(), self.deal_card()]
        self.game_over = False
        self.save()

    def player_hit(self):
        """
        Handles the player taking another card.

        Returns:
            str or None: A message if the player busts, otherwise None.
        """
        self.player_hand.append(self.deal_card())
        if self.calculate_hand(self.player_hand) > 21:
            self.game_over = True
            self.save()
            return "Bust! You lose."
        self.save()
        return None

    def dealer_play(self):
        """
        Handles the dealer's play and determines the outcome of the game.

        Returns:
            str: The outcome of the game.
        """
        while self.calculate_hand(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deal_card())

        player_score = self.calculate_hand(self.player_hand)
        dealer_score = self.calculate_hand(self.dealer_hand)

        self.game_over = True
        self.save()

        if dealer_score > 21:
            return "Dealer busts! You win!"
        elif dealer_score > player_score:
            return "Dealer wins!"
        elif dealer_score < player_score:
            return "You win!"
        else:
            return "It's a tie!"


from django.db import models
from django.contrib.auth.models import User


class UserBalance(models.Model):
    """
    Represents a user's balance.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=1000)

    def __str__(self):
        """
        Returns a string representation of the user's balance.

        Returns:
            str: The user's username and balance.
        """
        return f"{self.user.username}: {self.balance}"


class GameHistory(models.Model):
    """
    Represents the history of a game.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    initial_bet = models.IntegerField(default=0)
    outcome = models.CharField(max_length=50, null=True, blank=True)
    profit_loss = models.IntegerField(default=0)

    def __str__(self):
        """
        Returns a string representation of the game history.

        Returns:
            str: The user's username, start time, and outcome.
        """
        return f"{self.user.username} - {self.start_time} - {self.outcome}"