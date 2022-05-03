"""View module for handling requests about event"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action     # use for signup method
from levelupapi.models import Event
from levelupapi.models import Game
from levelupapi.models import Gamer

# use in create to validate receiving errors
from django.core.exceptions import ValidationError


class EventView(ViewSet):
    """Level up event view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event
        Returns:
            Response -- JSON serialized event
        """
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all events
        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all()
        game = request.query_params.get('game', None)
        gamer = Gamer.objects.get(user=request.auth.user)

        if game is not None:
            events = events.filter(game_id=game)

        # Set the `joined` property on every event
        for event in events:
            # Check to see if the gamer is in the attendees list on the event
            event.joined = gamer in event.attendees.all()
            if event.organizer.user == request.auth.user:
                event.is_organizer = True
            else:
                event.is_organizer = False

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


    def create(self, request):
        """Handle POST operations
        Returns
            Response -- JSON serialized event instance
        """
        organizer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data['game'])

        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(organizer=organizer, game=game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def update(self, request, pk):
    #     """(Is working)Handle PUT requests for a event
    #     Without validation
    #     """

    #     event = Event.objects.get(pk=pk)
    #     event.description = request.data["description"]
    #     event.date = request.data["date"]
    #     event.time = request.data["time"]

    #     game = Game.objects.get(pk=request.data["game"])
    #     event.game = game
    #     event.save()

    #     return Response(None, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        """Handle PUT requests for a event
        with validation
        """
        event = Event.objects.get(pk=pk)
        game = Game.objects.get(pk=request.data['game'])
        # The original event object is passed to the serializer, along with the request.data
        # This will make any updates on the event object
        serializer = CreateEventSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(game=game)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True)
    def leave(self, request, pk):
        """Delete request for a user to leave an event"""

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        return Response({'message': 'Gamer removed'}, status=status.HTTP_204_NO_CONTENT)


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = Event
        # Using depth to embed tables: fields need to revise to
        # 'organizer' instead of 'organizer_id'
        fields = ('id', 'game', 'organizer',
          'description', 'date', 'time', 'attendees', 'joined', 'is_organizer')
        depth = 2

class CreateEventSerializer(serializers.ModelSerializer):
    """use for create (validation received data from client)"""
    class Meta:
        model = Event
        fields = ['id', 'description', 'date', 'time', 'game']
