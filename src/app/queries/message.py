from app.models import Message


def create(
    *, conversation_id: int, recipient_id: int, sender_id: int, body: str
) -> Message:
    return Message.objects.create(
        conversation_id=conversation_id,
        recipient_id=recipient_id,
        sender_id=sender_id,
        body=body,
    )
