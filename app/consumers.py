import json

from channels.generic.websocket import AsyncWebsocketConsumer

from asgiref.sync import sync_to_async

from app.queries import message as message_queries


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        kwargs = self.scope.get("url_route", {}).get("kwargs")
        self.room_name = kwargs.get("room_name")
        self.room_group_name = f"chat_{self.room_name}"

        await self.accept()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    @sync_to_async
    def save_message(self, *, conversation_id, body, recipient_id):
        message_queries.create(
            conversation_id=conversation_id,
            recipient_id=recipient_id,
            sender_id=self.scope.get("user").id,
            body=body,
        )

    async def receive(self, *, text_data=None):
        text_data = json.loads(text_data)

        data = text_data.get("data", {})
        conversation_id = data.get("conversation_id")
        recipient_id = data.get("recipient_id")
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
            conversation_id=conversation_id, body=body, recipient_id=recipient_id
        )

    async def chat_message(self, event):
        text_data = {
            "body": event.get("body"),
            "name": event.get("name"),
        }

        await self.send(text_data=json.dumps(text_data))
