from django.db import models
from .game import Game
from .gamer import Gamer


class Event(models.Model):

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    description = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    organizer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(Gamer, related_name="gamer")

    # create a custom property named 'joined' for Event class
    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value

    @property
    def is_organizer(self):
        return self.__is_organizer

    @is_organizer.setter
    def is_organizer(self, value):
        self.__is_organizer = value
