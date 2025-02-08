import random

from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView

from .models import Game, Move
from .serializers import GameSerializer, MoveSerializer


# Create your views here.


class GameViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]
    queryset = Game.objects.all()

    def list(self, request):
        user = request.user
        queryset = user.game_set.all()
        serializer = GameSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = request.user
        queryset = user.game_set.all()
        game = get_object_or_404(queryset, pk=pk)
        game.calculate_winner()
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def create(self, request):
        user = request.user
        game = Game()
        game.player = user
        game.save()
        serializer = GameSerializer(game)
        return Response(serializer.data)


class MoveViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    serializer_class = MoveSerializer
    permission_classes = [IsAuthenticated]
    queryset = Move.objects.all()

    def list(self, request, game_id=None):
        game = get_object_or_404(Game, pk=game_id)
        moves = Move.objects.filter(game=game)
        serializer = MoveSerializer(moves, many=True)
        return Response(serializer.data)

    def create(self, request, game_id=None):
        game = get_object_or_404(Game, pk=game_id)
        if game.winner is not None:
            serializer = GameSerializer(game)
            return Response({"message": "Game is Over", "game": serializer.data})

        exists = Move.objects.filter(game=game, x=request.data['x'], y=request.data['y']).exists()
        if exists:
            return Response({'error': 'Move already exists'}, status=status.HTTP_400_BAD_REQUEST)

        move = Move()
        move.player = request.user.email
        move.game = game
        move.x = request.data.get("x")
        move.y = request.data.get("y")
        move.save()
        game.update_state(move.x,  move.y, "X")

        # Generate the computers random move
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        while Move.objects.filter(game=game, x=x, y=y).exists():
            x = random.randint(0, 2)
            y = random.randint(0, 2)

        comp_move = Move()
        comp_move.player = "cpu"
        comp_move.game = game
        comp_move.x = x
        comp_move.y = y
        comp_move.save()
        game.update_state(comp_move.x, comp_move.y, "O")

        winner = game.calculate_winner()
        if winner is not None:
            if game.winner == "TRUE":
                return Response({"message": "Congratulations, you have won the game", "board": game.state})
            elif game.winner == "FALSE":
                return Response({"message": "Sorry, you have lost the game", "board": game.state})
            else:
                return Response({"message": "Game Over, DRAW", "board": game.state})

        serializer = MoveSerializer(comp_move)
        return Response(serializer.data)
