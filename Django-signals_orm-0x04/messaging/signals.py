
# messaging/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import Message, Notification

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