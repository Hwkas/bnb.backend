# Generated by Django 5.0.6 on 2024-06-13 19:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0002_reservation'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='favourited',
            field=models.ManyToManyField(blank=True, related_name='favourites', to=settings.AUTH_USER_MODEL),
        ),
    ]
