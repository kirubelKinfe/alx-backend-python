from django.db import models

class UnreadMessagesManager(models.Manager):
    """Custom manager for unread messages"""
    def for_user(self, user):
        return self.get_queryset().filter(
            receiver=user,
            read=False
        ).select_related('sender').only(
            'message_id',
            'sender__username',
            'content',
            'timestamp'
        )