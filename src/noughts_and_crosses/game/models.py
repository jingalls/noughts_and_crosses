import numpy as np
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Game(models.Model):
    player = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    winner = models.CharField(max_length=5, null=True, blank=True, choices=[('TRUE', 'True'),
                                                                            ('FALSE', 'False'),
                                                                            ('DRAW', 'Draw')])
    state = models.JSONField(default=list)

    def check_rows(self, board):
        for row in board:
            if len(set(row)) == 1:
                self.winner = "TRUE" if row[0] == 'X' else 'FALSE'
                return 1

        return 0

    def check_diagnals(self, board):
        if len(set([board[i][i] for i in range(len(board))])) == 1:
            self.winner = "TRUE" if board[0][0] == 'X' else 'FALSE'
            return 1
        if len(set([board[i][len(board) - i - 1] for i in range(len(board))])) == 1:
            self.winner = "TRUE" if board[0][len(board) - 1] == 'X' else "FALSE"
            return 1
        return 0

    def calculate_winner(self):
        if len(self.move_set.all()) < 6:
            return

        board = self.state
        for newBoard in [board, np.transpose(board)]:
            result = self.check_rows(newBoard)
            if result:
                self.save()
                return self.winner

            result = self.check_diagnals(newBoard)
            if result:
                self.save()
                return self.winner

        if len(self.move_set.all()) == 9 and not self.winner:
            self.winner = "DRAW"

        return self.winner or None

    def update_state(self, x, y, value):
        current_state = self.state
        if not current_state:
            current_state = [['_', '_', '_'],
                             ['_', '_', '_'],
                             ['_', '_', '_']]

        current_state[y][x] = value
        self.state = current_state

        self.save()


class Move(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.CharField(max_length=50)
    x = models.IntegerField(null=False, blank=False,
                            validators=[
                                MinValueValidator(0),
                                MaxValueValidator(2)
                            ])
    y = models.IntegerField(null=False, blank=False,
                            validators=[
                                MinValueValidator(0),
                                MaxValueValidator(2)
                            ])




