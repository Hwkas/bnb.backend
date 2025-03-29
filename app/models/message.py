from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.conversation import Conversation
from app.models.user import User


class Message(models.Model):
    conversation = models.ForeignKey(
        verbose_name=_("conversaition"),
        to=Conversation,
        related_name="messages",
        on_delete=models.CASCADE,
    )
    body = models.TextField(verbose_name=_("body"))
    recipient = models.ForeignKey(
        verbose_name=_("recipient"),
        to=User,
        related_name="received_messages",
        on_delete=models.CASCADE,
    )
    sender = models.ForeignKey(
        verbose_name=_("sender"),
        to=User,
        related_name="sent_messages",
        on_delete=models.CASCADE,
    )
    create_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now_add=True,
    )

    def __str__(self):
        return f"sender: {self.sender} - recipient: {self.recipient}"

    class Meta:
        app_label = "app"
        verbose_name = _("message")
        verbose_name_plural = _("messages")
