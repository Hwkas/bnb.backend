from contextlib import suppress
from typing import List, Union

from rest_framework.exceptions import ValidationError

from app.models import Conversation


def filter(*, user_id: int) -> List[Conversation]:
    return Conversation.objects.filter(users__id=user_id)


def create(*, user_id1: int, user_id2: int) -> Conversation:
    conversation = Conversation.objects.create()
    conversation.users.add(user_id1)
    conversation.users.add(user_id2)
    return conversation


def get(*, id: int) -> Conversation:
    with suppress(Conversation.DoesNotExist):
        return Conversation.objects.get(id=id)
    raise ValidationError(
        detail={"error": "conversation doesn't exists."}, code="conversation"
    )


def filter_group(*, user_id1: int, user_id2: int) -> Union[Conversation | None]:
    return (
        Conversation.objects.filter(users__id=user_id1)
        .filter(users__id=user_id2)
        .first()
    )
