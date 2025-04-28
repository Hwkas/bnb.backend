from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    avatar = models.ImageField(
        verbose_name=_("avatar"),
        upload_to="uploads/avatar",
        null=True,
        blank=True,
    )

    def avatar_url(self) -> str:
        return f"{settings.WEBSITE_URL}{self.avatar.url}" if self.avatar else ""

    def __str__(self):
        return self.username

    class Meta:
        app_label = "app"
        verbose_name = _("user")
        verbose_name_plural = _("users")
