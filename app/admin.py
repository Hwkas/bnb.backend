from django.contrib import admin

from app.models import Conversation, Message, Property, Reservation, User


# Register your models here.
admin.site.register(
    model_or_iterable=[
        User,
        Property,
        Reservation,
        Conversation,
        Message,
    ]
)
