from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json
import logging

logger = logging.getLogger(__name__)


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close
        else:
            self.room_name = f"private_chat_{self.user.username}"
            self.room_group_name = f"private_chat_{self.room_name}"
            logger.info('websocket connected to backend')

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        logger.info('websocket group add')

        await self.accept()
        logger.info('accepted')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
        logger.info('disconneted')

    async def receive (self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        print("message type: ", message_type)
        message = text_data_json['message']
        logger.info('message received from websocket frontend: %s', message)

        if message_type == 'chat_message':
            recipients = text_data_json['recipients']
            logger.info('recipients: %s', recipients)
            for recipient in recipients:
                logger.info('recipient: %s', recipient)
                reci_channel_name = f"private_chat_private_chat_{recipient}"
                await self.channel_layer.group_send(
                    reci_channel_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                    }
                )
        logger.info('broadcast signal transferred to chat_message functon')

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({'type': 'chat_message', 'message': message}))
        logger.info('message sent to websocket frontend: %s', message)


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
        message_type = text_data_json.get('type')
        print("message type: ", message_type)
        message = text_data_json['message']
        logger.info('message received from websocket frontend')

        if message_type == 'chat.message':
            pass

        if message_type == 'group.message':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'group.message',
                    'message': message,
                }
            )


    async def send_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({'type': 'group.message', 'message': message}))
