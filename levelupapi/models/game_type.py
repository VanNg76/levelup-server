from django.db import models


class Game_Type(models.Model):

    label = models.CharField(max_length=20)
