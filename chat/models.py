import uuid

from django.db import models

from accounts.models import User


class Conversation(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    users = models.ManyToManyField(User, related_name="conversations")
    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)


class ConversationMessage(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    conversation = models.ForeignKey(
        Conversation,
        related_name="messages",
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    recipient = models.ForeignKey(
        User,
        related_name="received_messages",
        on_delete=models.CASCADE,
    )
    sender = models.ForeignKey(
        User,
        related_name="sent_messages",
        on_delete=models.CASCADE,
    )
    create_at = models.DateTimeField(auto_now_add=True)
