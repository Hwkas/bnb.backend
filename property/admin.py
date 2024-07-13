from django.contrib import admin

# my models
from .models import Property, Reservation

# Register your models here.

admin.site.register(Property)
admin.site.register(Reservation)
