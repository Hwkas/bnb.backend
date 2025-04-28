from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.user import User


class Conversation(models.Model):
    users = models.ManyToManyField(
        verbose_name=_("user"),
        to=User,
        related_name="conversations",
    )
    create_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now_add=True,
    )
    modified_at = models.DateTimeField(
        verbose_name=_("modified at"),
        auto_now=True,
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = "app"
        verbose_name = _("conversation")
        verbose_name_plural = _("conversations")
