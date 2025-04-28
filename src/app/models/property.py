from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.user import User


class Property(models.Model):
    title = models.CharField(
        verbose_name=_("title"),
        max_length=255,
    )
    description = models.TextField(verbose_name=_("description"))
    price_per_night = models.IntegerField(verbose_name=_("price per night"))
    bedrooms = models.IntegerField(verbose_name=_("number of bedrooms"))
    bathrooms = models.IntegerField(verbose_name=_("number of bathrooms"))
    guests = models.IntegerField(verbose_name=_("number of guests"))
    country = models.CharField(
        verbose_name=_("country"),
        max_length=255,
    )
    country_code = models.CharField(
        verbose_name=_("country code"),
        max_length=10,
    )
    category = models.CharField(
        verbose_name=_("category"),
        max_length=255,
    )
    favourited = models.ManyToManyField(
        verbose_name=_("favourited"),
        to=User,
        related_name="favourites",
        blank=True,
    )
    image = models.ImageField(
        verbose_name=_("image"),
        upload_to="uploads/properties",
    )
    landlord = models.ForeignKey(
        verbose_name=_("landlord"),
        to=User,
        related_name="properties",
        on_delete=models.CASCADE,
    )
    created_at = models.DateField(
        verbose_name=_("created at"),
        auto_now_add=True,
    )

    def image_url(self):
        return f"{settings.WEBSITE_URL}{self.image.url}"

    def __str__(self):
        return f"landlord: {self.landlord.username} - property: {self.title}"

    class Meta:
        app_label = "app"
        verbose_name = _("property")
        verbose_name_plural = _("properties")
