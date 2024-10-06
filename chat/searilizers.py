from rest_framework import serializers

from accounts.searilizers import UserDetailSearilizer

from .models import Conversation, ConversationMessage


class ConversationListSearilizer(serializers.ModelSerializer):
    users = UserDetailSearilizer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = (
            "id",
            "users",
            "modified_at",
        )


class ConversationDetailSearilizer(serializers.ModelSerializer):
    users = UserDetailSearilizer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = (
            "id",
            "users",
            "modified_at",
        )


class ConversationMessageSearilizer(serializers.ModelSerializer):
    send_to = UserDetailSearilizer(many=False, read_only=True)
    created_by = UserDetailSearilizer(many=False, read_only=True)

    class Meta:
        model = ConversationMessage
        fields = (
            "id",
            "body",
            "send_to",
            "created_by",
        )
