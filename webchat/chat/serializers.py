from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Thread, Message


class UserSerializer(serializers.ModelSerializer):
    """User serializer. The necessary solution for the correct operation of the program"""
    class Meta:
        model = User
        fields = ("id", "username")


class ThreadSerializer(serializers.ModelSerializer):
    """Thread serializer. """

    participant = UserSerializer(many=True)
    unread_messages_count = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ("id", "participant",
                  "created", 'unread_messages_count')

    # Function to calculate the number of unread messages

    def get_unread_messages_count(self, thread):
        return len(Message.objects.filter(
            thread=thread, is_read=False))


class MessageSerializer(serializers.ModelSerializer):
    """ Default serializer for messages. """
    sender = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'thread', 'sender', 'text', 'created', 'is_read')


class MessagePostSerializer(serializers.ModelSerializer):
    """ Special serializer for some POST methods for messages"""
    thread = serializers.IntegerField()
    text = serializers.CharField(max_length=500)

    class Meta:
        model = Message
        fields = ('thread', 'text', 'sender')
