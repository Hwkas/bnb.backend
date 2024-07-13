# lib import
import uuid

# django imports
from django.db import models
from django.conf import settings
from accounts.models import User


class Property(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    guests = models.IntegerField()
    country = models.CharField(max_length=255)
    country_code = models.CharField(max_length=10)
    category = models.CharField(max_length=255)
    favourited = models.ManyToManyField(
        User,
        related_name="favourites",
        blank=True,
    )
    image = models.ImageField(upload_to="uploads/properties")
    landlord = models.ForeignKey(
        to=User,
        related_name="properties",
        on_delete=models.CASCADE,
    )
    created_at = models.DateField(auto_now_add=True)

    def image_url(self):
        return f"{settings.WEBSITE_URL}{self.image.url}"


class Reservation(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    property = models.ForeignKey(
        Property,
        related_name="reservations",
        on_delete=models.CASCADE,
    )
    created_by = models.ForeignKey(
        User,
        related_name="reservations",
        on_delete=models.CASCADE,
    )
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_nights = models.IntegerField()
    guests = models.IntegerField()
    total_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)