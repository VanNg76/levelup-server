"""View module for handling requests about event"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
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
        if game is not None:
            events = events.filter(game_id=game)

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


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = Event
        # Using depth to embed tables: fields need to revise to
        # 'organizer' instead of 'organizer_id'
        fields = ('id', 'description', 'date', 'time', 'game', 'organizer')
        depth = 2

class CreateEventSerializer(serializers.ModelSerializer):
    """use for create (validation received data from client)"""
    class Meta:
        model = Event
        fields = ['id', 'description', 'date', 'time', 'game']
