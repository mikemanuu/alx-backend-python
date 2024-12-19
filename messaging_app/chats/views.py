from django.shortcuts import render
from rest_framework import viewsets, status
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


# Conversation ViewSet
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.prefetch_related(
        'participants', 'messages').all()
    serializer_class = ConversationSerializer

    @action(detail=False, methods=['post'], url_path='create')
    def create_conversation(self, request):
        participants_ids = request.data.get('participants')
        if not participants_ids or len(participants_ids) < 2:
            return Response(
                {"error": "A conversation must have at least two participants."},
                status=status.HTTP_400_BAD_REQUEST
            )
        participants = User.objects.filter(user_id__in=participants_ids)
        if participants.count() < len(participants_ids):
            return Response(
                {"error": "Some participants were not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Message ViewSet
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related('sender', 'conversation').all()
    serializer_class = MessageSerializer

    @action(detail=True, methods=['post'], url_path='send')
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        serializer = MessageCreateSerializer(data=request.data)
        if serializer.is_valid():
            sender_id = serializer.validated_data['sender']
            message_body = serializer.validated_data['message_body']
            sender = User.objects.get(user_id=sender_id)
            message = Message.objects.create(
                sender=sender,
                conversation=conversation,
                message_body=message_body
            )
            return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
