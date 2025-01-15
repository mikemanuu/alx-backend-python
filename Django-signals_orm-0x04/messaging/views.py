from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Message


@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('home')
    return redirect('profile')


def threaded_conversations(request):
    messages = Message.objects.filter(parent_message__isnull=True).select_related(
        'sender', 'receiver').prefetch_related('replies')

    return render(request, 'threaded_conversations.html', {'messages': messages})


def view_thread(request, message_id):
    message = Message.objects.get(id=message_id)
    replies = message.get_all_replies()

    return render(request, 'message_thread.html', {'message': message, 'replies': replies})


def inbox(request):
    user = request.user
    unread_messages = Message.unread.for_user(user)

    return render(request, 'inbox.html', {'unread_messages': unread_messages})


def view_message_history(request, message_id):
    message = Message.objects.get(id=message_id)
    history = message.history.all().select_related('edited_by')
    return render(request, 'message_history.html', {'message': message, 'history': history})
