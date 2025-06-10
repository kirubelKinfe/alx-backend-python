
# messaging/signals.py
from datetime import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Creates a notification when a new message is sent.
    """
    if created:
        Notification.objects.create(
            recipient=instance.receiver,
            sender=instance.sender,
            message=f"New message from {instance.sender.username}",
            content_object=instance  # Links to the Message
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Logs message edits by comparing old and new content.
    Creates a MessageHistory record when content changes.
    """
    if instance.pk:  # Only for existing messages (edits)
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:  # Content changed
                MessageHistory.objects.create(
                    original_message=instance,
                    old_content=old_message.content,
                    edited_by=instance.sender
                )
                instance.edited = True
                instance.last_edited = timezone.now()
        except Message.DoesNotExist:
            pass  # New message being created