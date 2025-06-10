import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class Message(models.Model):
    """Model to represent a message in a conversation."""
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="Unique identifier for the message")
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text="The user who sent this message"
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receive_messages',
        help_text="The user who receive this message"
    )
    content = models.TextField(max_length=2000, help_text="Message content")
    timestamp = models.DateTimeField(default=timezone.now, help_text="When the message was sent")
    
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender.username}"
    

class Notification(models.Model):
    """Model to store user notifications"""
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text="User who receives the notification"
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sent_notifications',
        help_text="User who triggered the notification"
    )
    message = models.CharField(
        max_length=255,
        help_text="Notification content"
    )
    is_read = models.BooleanField(
        default=False,
        help_text="Whether the notification has been read"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the notification was created"
    )
    
    # Generic foreign key to link to any model (like Message)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"Notification for {self.recipient.username}"