from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Conversation, user, Message
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsParticipant, IsParticipantOfConversation
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .filters import MessageFilter

# Create your views here.


class MessagePagination(PageNumberPagination):
    """
    Custom pagination for messages.
    """
    page_size = 20


class ConversationListView(APIView):
    def get(self, request):
        conversations = Conversation.objects.all()
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['participants']
    ordering_fields = ['created_at']
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    @action(detail=False, methods=['post'], url_path='create')
    def create_conversation(self, request):
        # Existing logic for creating a conversation
        ...

    def get_queryset(self):
        # Filter conversations where the user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participants_info = request.data.get('participants', [])
        if len(participants_info) < 2:
            return Response({"error": "Participants should be more than 1."}, status=status.HTTP_400_BAD_REQUEST)

        participants = User.objects.filter(user_id__in=participants_info)

        if participants.count() != len(participants_info):
            return Response({"error": "Participants are not more than 1."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new conversation and add participants
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sender', 'conversation']
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filterset_class = MessageFilter

    @action(detail=True, methods=['post'], url_path='send')
    def send_message(self, request, pk=None):
        # Existing logic for sending a message
        ...

    def get_queryset(self):
        # Filter messages related to conversations the user participates in
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        sender_id = request.data.get('sender')
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body')

        sender = User.objects.get(user_id=sender_id)
        conversation = Conversation.objects.get(
            conversation_id=conversation_id)

        if len(message_body) > 500:
            return Response({"error": "Message cannot be more than 500 characters."}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            sender=sender, conversation=conversation, message_body=message_body)

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
