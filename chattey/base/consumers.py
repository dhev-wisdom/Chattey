from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        username = self.scope['url_route']['kwargs']['username']
        self.room_name = f"private_chat_{username}"
        self.room_group_name = f"private_chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive (self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message,
            }
        )

    async def send_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({'message': message}))


class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_name = f"group_chat_{room_id}"
        self.room_group_name = f"group_chat_{self.room_name}"

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

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'group.message',
                'message': message,
            }
        )

    async def send_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({'message': message}))
