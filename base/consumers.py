from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
import json
import logging
from .models import Message, ChatRoom
from django.contrib.auth.models import User

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

    @sync_to_async
    def save_message(self, body, sender, receiver):
        user_sender = User.objects.get(username=sender)
        user_receiver = User.objects.get(username=receiver)
        message = Message(
            body = body,
            sender = user_sender,
            receiver = user_receiver,
        )
        message.save()
        print(message)
        logger.info('message %s', message)
        return message.id
    
    @sync_to_async
    def get_message(self, id):
        message = Message.objects.get(id=id)
        return message

    async def receive (self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        message = text_data_json['message']
        recipients = text_data_json['recipients']
        message_sender = recipients[0]
        message_id = await self.save_message(message, recipients[0], recipients[1])
        message_ = await self.get_message(message_id)


        logger.info('message received from websocket frontend: %s', message)

        if message_type == 'chat_message':
            logger.info('recipients: %s', recipients)
            for recipient in recipients:
                logger.info('recipient: %s', recipient)
                reci_channel_name = f"private_chat_private_chat_{recipient}"
                await self.channel_layer.group_send(
                    reci_channel_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'sender': message_sender,
                        'id': message_id,
                        'time': message_.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                        'is_read': message_.is_read,
                        'is_deleted': message_.is_deleted,
                        'is_edited': message_.is_edited,
                    }
                )
        logger.info('broadcast signal transferred to chat_message functon')

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        time = event['time']
        is_read = event['is_read']
        is_edited = event['is_edited']
        is_deleted = event['is_deleted']
        id = event['id']

        await self.send(text_data=json.dumps({
            'type': 'chat_message', 'message': message, 'sender': sender, 'time': time,
            'is_read': is_read, 'is_edited': is_edited, 'is_deleted': is_deleted, 'id': id,
            }))
        logger.info('message sent to websocket frontend: %s', message)


class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        room_id = self.scope['url_route']['kwargs']['id']
        self.room_name = f"group_chat_{room_id}"
        self.room_group_name = f"group_chat_{self.room_name}"
        logger.info('websocket connected to backend')

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()
        logger.info('accepted')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
        logger.info('websocket disconnected')

    @sync_to_async
    def save_message(self, body, sender, room_id):
        user_sender = User.objects.get(username=sender)
        room = ChatRoom.objects.get(id=room_id)
        message = Message(
            body = body,
            sender = user_sender,
            room = room,
        )
        message.save()
        return message.id
    
    @sync_to_async
    def get_message(self, id):
        message = Message.objects.get(id=id)
        return message
    
    @sync_to_async
    def get_sender(self, username):
        sender = User.objects.get(username=username)
        return sender.id

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        sender = text_data_json.get('sender')
        sender_id = await self.get_sender(sender)
        room_id = text_data_json.get('room_id')
        print("message type: ", message_type)
        message = text_data_json['message']
        message_id = await self.save_message(message, sender, room_id)
        message_ = await self.get_message(message_id)
        logger.info('message saved to database for room %s', room_id)
        logger.info('message received from websocket frontend for room: %s', room_id)

        if message_type == 'group_message':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'group_message',
                    'room_id': room_id,
                    'message': message,
                    'sender': sender,
                    'sender_id': sender_id,
                    'time': message_.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'is_read': message_.is_read,
                    'is_deleted': message_.is_deleted,
                    'is_edited': message_.is_edited,
                }
            )
        logger.info('broadcast signal transferred to group_message functon')


    async def group_message(self, event):
        message = event['message']
        room_id = event['room_id']
        sender = event['sender']
        sender_id = event['sender_id']
        time = event['time']
        is_read = event['is_read']
        is_edited = event['is_edited']
        is_deleted = event['is_deleted']

        await self.send(text_data=json.dumps({
            'type': 'group_message',
            'message': message,
            'room_id': room_id,
            'sender': sender,
            'sender_id': sender_id,
            'is_read': is_read,
            'is_edited': is_edited,
            'is_deleted': is_deleted,
            'time': time,
            }))
