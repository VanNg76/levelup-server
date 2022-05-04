from django.db import models
from .game import Game
from .gamer import Gamer


class Event(models.Model):
    # add related_name='events' to attached a 'events' prop into game
    # now we can use 'Count' events on GameView 
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="events")
    description = models.CharField(max_length=20)
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField()
    organizer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(Gamer, related_name="gamers")

    # create a custom property named 'joined' for Event class
    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value

    # create another custom property to return to client to
    # check if current logged in user is organizer of an event
    @property
    def is_organizer(self):
        return self.__is_organizer

    @is_organizer.setter
    def is_organizer(self, value):
        self.__is_organizer = value
