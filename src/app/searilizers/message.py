from rest_framework import serializers

from app.models import Message
from app.searilizers.user import UserDetailSearilizer


class MessageSearilizer(serializers.ModelSerializer):
    recipient = UserDetailSearilizer(many=False, read_only=True)
    sender = UserDetailSearilizer(many=False, read_only=True)

    class Meta:
        model = Message
        fields = (
            "id",
            "body",
            "recipient",
            "sender",
        )
