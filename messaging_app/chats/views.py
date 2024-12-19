from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Conversation, User, Message
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer

# Create your views here.


class ConversationListView(APIView):
    def get(self, request):
        conversations = Conversation.objects.all()
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.prefetch_related(
        'participants', 'messages').all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__first_name', 'participants__last_name']
    ordering_fields = ['created_at']

    @action(detail=False, methods=['post'], url_path='create')
    def create_conversation(self, request):
        # Existing logic for creating a conversation
        ...


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related('sender', 'conversation').all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['sender__first_name', 'sender__last_name', 'message_body']
    ordering_fields = ['sent_at']

    @action(detail=True, methods=['post'], url_path='send')
    def send_message(self, request, pk=None):
        # Existing logic for sending a message
        ...
