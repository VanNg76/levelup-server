from django.db import models

from .game_type import Game_Type
from .gamer import Gamer


class Game(models.Model):

    game_type = models.ForeignKey(Game_Type, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    maker = models.CharField(max_length=20)
    gamer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    number_of_player = models.IntegerField
    skill_level = models.IntegerField
