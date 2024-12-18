from rest_framework import serializers
from .models import User, Message, Conversation
from .serializers import UserSerializer, MessageSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import SerializerMethodField


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name',
                  'email', 'phone_number', 'role', 'created_at']


# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    time_since_sent = SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender',
                  'message_body', 'sent_at', 'time_since_sent']

    def get_time_since_sent(self, obj):
        from datetime import datetime
        time_diff = datetime.now() - obj.sent_at
        return str(time_diff.days) + " days ago"


# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']


# Custom Validation to ensure that a user cannot be both sender and receiver)
class MessageCreateSerializer(serializers.ModelSerializer):
    sender = serializers.UUIDField()
    receiver = serializers.UUIDField()

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message_body', 'sent_at']

    def validate(self, data):
        if data['sender'] == data['receiver']:
            raise ValidationError("Sender and receiver cannot be the same.")
        return data
