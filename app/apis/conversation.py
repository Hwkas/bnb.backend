from django.http import JsonResponse

from rest_framework.decorators import api_view

from app.queries import conversation as conversation_queries
from app.searilizers import (
    ConversationListSearilizer,
    MessageSearilizer,
)


@api_view(["GET"])
def list(request) -> JsonResponse:
    searilizer = ConversationListSearilizer(
        conversation_queries.filter(user_id=request.user.id),
        many=True,
        context={"username": request.user.username},
    )
    return JsonResponse(searilizer.data, safe=False)


@api_view(["GET"])
def detail(request, id: int) -> JsonResponse:
    conversation = conversation_queries.get(id=id)

    conversation_searilizer = ConversationListSearilizer(conversation, many=False)
    messages_searilizer = MessageSearilizer(conversation.messages.all(), many=True)
    return JsonResponse(
        {
            "conversation": conversation_searilizer.data,
            "messages": messages_searilizer.data,
        },
        safe=False,
    )


@api_view(["GET"])
def start(request, user_id: int) -> JsonResponse:
    conversation = conversation_queries.filter_group(
        user_id1=request.user.id, user_id2=user_id
    )

    if not conversation:
        conversation = conversation_queries.create(
            user_id1=user_id, user_id2=request.user.id
        )
    return JsonResponse({"success": True, "conversation_id": conversation.id})
