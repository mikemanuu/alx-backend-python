from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Conversation
from .serializers import ConversationSerializer

# Create your views here.


class ConversationListView(APIView):
    def get(self, request):
        conversations = Conversation.objects.all()
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)
