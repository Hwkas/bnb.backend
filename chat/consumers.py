import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import ConversationMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        kwargs = self.scope.get("url_route", {}).get("kwargs")
        self.room_name = kwargs.get("room_name")
        self.room_group_name = f"chat_{self.room_name}"

        # Join Room

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    @sync_to_async
    def save_message(self, *, conversation_id, body, sent_to_id):
        ConversationMessage.objects.create(
            conversation_id=conversation_id,
            body=body,
            send_to_id=sent_to_id,
            created_by=self.scope.get("user"),
        )

    async def receive(self, text_data=None):
        text_data = json.loads(text_data)

        data = text_data.get("data", {})
        conversation_id = data.get("conversation_id")
        sent_to_id = data.get("sent_to_id")
        name = data.get("name")
        body = data.get("body")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "body": body,
                "name": name,
            },
        )

        await self.save_message(
            conversation_id=conversation_id, body=body, sent_to_id=sent_to_id
        )

    async def chat_message(self, event):
        text_data = {
            "body": event.get("body"),
            "name": event.get("name"),
        }

        await self.send(text_data=json.dumps(text_data))
