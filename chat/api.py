from django.http import JsonResponse

from rest_framework.decorators import api_view

from .models import Conversation
from .searilizers import (
    ConversationDetailSearilizer,
    ConversationListSearilizer,
    ConversationMessageSearilizer,
)


@api_view(["GET"])
def conversations_list(request) -> JsonResponse:
    searilizer = ConversationListSearilizer(
        request.user.conversations.all(),
        many=True,
    )
    return JsonResponse(searilizer.data, safe=False)


@api_view(["GET"])
def conversations_detail(request, pk: int) -> JsonResponse:
    conversation = request.user.conversations.get(pk=pk)

    conversation_searilizer = ConversationDetailSearilizer(conversation, many=False)
    messages_searilizer = ConversationMessageSearilizer(
        conversation.messages.all(), many=True
    )
    return JsonResponse(
        {
            "conversation": conversation_searilizer.data,
            "messages": messages_searilizer.data,
        },
        safe=False,
    )


@api_view(["GET"])
def conversations_start(request, user_id: int) -> JsonResponse:
    conversations = Conversation.objects.filter(users__id__in=[request.user.id]).filter(
        users__id__in=[user_id]
    )

    if conversations.exists():
        conversation = conversations.first()
    else:
        conversation = Conversation.objects.create()
        conversation.users.add(user_id)
        conversation.users.add(request.user.id)
    return JsonResponse({"success": True, "conversation_id": conversation.id})
