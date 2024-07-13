from rest_framework import serializers

from .models import User


class UserDetailSearilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "avatar_url",
        )
