import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messaging_sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messaging_received_messages')
    content = models.TextField(max_length=2000)
    timestamp = models.DateTimeField(default=timezone.now)
    edited = models.BooleanField(default=False)  # New field to track edits
    last_edited = models.DateTimeField(null=True, blank=True)  # When last edited

    def __str__(self):
        return f"Message from {self.sender.username}"

class MessageHistory(models.Model):
    """Stores historical versions of edited messages"""
    original_message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='edits'
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='message_edits'
    )

    class Meta:
        ordering = ['-edited_at']
        verbose_name_plural = "Message History"

    def __str__(self):
        return f"Edit of {self.original_message} at {self.edited_at}"
    

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