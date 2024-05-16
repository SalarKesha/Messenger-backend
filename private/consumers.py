import socket

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from private.models import PrivateChat, PrivateMessage
from private.serializers import PrivateMessageSerializer, PrivateMessageCreateSerializer
from django.utils import timezone


class PrivateChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.private_chat_id = self.scope['url_route']['kwargs']['private_chat_id']
        self.chat_room_id = f"pv_{self.private_chat_id}"
        if not self.user.is_authenticated:
            await self.close()
        if await self.check_permission(self.user):
            await self.update_last_visit(user=self.user)
            await self.channel_layer.group_add(self.chat_room_id, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, code):
        await self.update_last_visit(user=self.user)
        await self.channel_layer.group_discard(self.chat_room_id, self.channel_name)

    async def receive_json(self, content, **kwargs):
        private_message = await self.save_private_message(user=self.user, content=content)
        if private_message:
            await self.channel_layer.group_send(
                self.chat_room_id,
                {'type': 'send_private_message', 'private_message': private_message}
            )

    async def send_private_message(self, event):
        await self.send_json(content={'message': event.get('private_message')})

    @database_sync_to_async
    def save_private_message(self, user, content):
        data = {
            'private_chat': self.private_chat_id,
            'sender': user.id,
            'type': content.get('message_type'),
            'content': content.get('text')
        }
        serializer = PrivateMessageCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return False

    @database_sync_to_async
    def check_permission(self, user):
        try:
            private_chat = PrivateChat.objects.get(id=self.private_chat_id)
            if private_chat.owner == user or private_chat.user == user:
                return True
            return False
        except PrivateChat.DoesNotExist:
            return False

    @database_sync_to_async
    def update_last_visit(self, user):
        private_chat = PrivateChat.objects.filter(id=self.private_chat_id).first()
        if private_chat:
            if private_chat.owner == user:
                private_chat.owner_last_visit = timezone.now()
            else:
                private_chat.user_last_visit = timezone.now()
            private_chat.save()
