from django.db import models
from django.contrib.auth.models import User

# Custom manager for unread messages


class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Return unread messages for the specified user.
        """
        return self.filter(receiver=user, read=False).only('id', 'sender', 'content', 'timestamp')


# Message model
class Message(models.Model):
    sender = models.ForeignKey(
        User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(
        null=True, blank=True)  # Timestamp of last edit
    edited_by = models.ForeignKey(  # User who made the last edit
        User, null=True, blank=True, related_name='edited_messages', on_delete=models.SET_NULL
    )
    parent_message = models.ForeignKey(
        'self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE
    )
    read = models.BooleanField(default=False)

    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom manager for unread messages

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"

    def get_all_replies(self):
        """
        Recursively fetch all replies to this message.
        """
        replies = self.replies.all().select_related('sender', 'receiver')
        all_replies = list(replies)
        for reply in replies:
            all_replies.extend(reply.get_all_replies())
        return all_replies


# Notification model
class Notification(models.Model):
    user = models.ForeignKey(
        User, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user}"


# MessageHistory model
class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message, related_name='history', on_delete=models.CASCADE)
    old_content = models.TextField()
    timestamp = models.DateTimeField(
        auto_now_add=True)  # When the edit occurred
    edited_by = models.ForeignKey(  # Who edited the message
        User, null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"History for Message ID {self.message.id}"
