from django.views.decorators.cache import cache_page
from django.shortcuts import render
from .models import Message


@cache_page(60)  # Cache the view for 60 seconds
def conversation_view(request, conversation_id):
    """
    Display a list of messages in a conversation.
    """
    # Fetch messages for the specified conversation
    messages = Message.objects.filter(
        parent_message__isnull=True).prefetch_related('replies')

    return render(request, 'conversation.html', {'messages': messages})
