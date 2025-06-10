import uuid
from django.db import models
from django.utils import timezone
from chats.models import User


class Message(models.Model):
    """Model to represent a message in a conversation."""
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="Unique identifier for the message")
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='messaging_sent_messages',
        help_text="The user who sent this message"
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='messaging_receive_messages',
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