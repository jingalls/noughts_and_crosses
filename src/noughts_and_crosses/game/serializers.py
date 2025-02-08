from .models import Game, Move
from django.contrib.auth.models import User
from rest_framework import serializers


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'player', 'state', 'winner']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class MoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Move
        fields = ['game', 'player', 'x', 'y']
