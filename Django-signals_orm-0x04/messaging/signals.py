from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory


@receiver(pre_save, sender=Message)
def log_message_edits(sender, instance, **kwargs):
    if instance.pk:  # Check if the message exists (not a new instance)
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:  # Check if content is edited
                # Log old content to MessageHistory
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content,
                    edited_by=instance.edited_by,  # Capture the editor
                )
                # Mark as edited and update the timestamp
                instance.edited = True
                instance.edited_at = timezone.now()
        except Message.DoesNotExist:
            pass
