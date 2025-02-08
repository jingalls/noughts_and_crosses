from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Game(models.Model):
    player = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    winner = models.CharField(max_length=5, null=True, blank=True, choices=[('TRUE', 'True'),
                                                                            ('FALSE', 'False'),
                                                                            ('DRAW', 'Draw')])

    def calculate_winner(self):
        moves = self.move_set()


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
