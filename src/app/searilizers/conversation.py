from rest_framework import serializers

from app.models import Conversation
from app.searilizers.user import UserDetailSearilizer


class ConversationListSearilizer(serializers.ModelSerializer):
    users = UserDetailSearilizer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = (
            "id",
            "users",
            "modified_at",
        )
