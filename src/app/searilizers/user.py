from rest_framework import serializers

from app.models import User


class UserDetailSearilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "avatar_url",
        )
