from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.utils import timezone

from channel.models import Channel, ChannelMember, ChannelMessage
from channel.serializers import ChannelMessageSerializer, ChannelMessageListSerializer


class ChannelConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get('user')
        self.channel_id = self.scope.get('url_route').get('kwargs').get('channel_id')
        self.chat_room_id = f"cc_{self.channel_id}"
        if not self.user.is_authenticated:
            await self.close()
            # return
        self.channel_member = await self.get_channel_member(self.user)
        if self.channel_member:
            await self.channel_layer.group_add(self.chat_room_id, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, code):
        await self.update_last_visit(self.channel_member)
        await self.channel_layer.group_discard(self.chat_room_id, self.channel_name)

    async def receive_json(self, content, **kwargs):
        if self.channel_member.type == ChannelMember.ADMIN:
            channel_message = await self.save_channel_message(content=content, sender=self.channel_member)
            if channel_message:
                await self.channel_layer.group_send(
                    self.chat_room_id,
                    {'type': 'send_channel_message', 'channel_message': channel_message}
                )

    async def send_channel_message(self, event):
        await self.send_json(content={'message': event.get('channel_message')})

    @database_sync_to_async
    def get_channel_member(self, user):
        return ChannelMember.objects.filter(channel_id=self.channel_id, user=user).first()

    @database_sync_to_async
    def save_channel_message(self, content, sender):
        data = {
            'channel': sender.channel.id,
            'sender': sender.id,
            'content': content.get('text')
        }
        serializer = ChannelMessageSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            return ChannelMessageListSerializer(instance).data
        return False

    @database_sync_to_async
    def update_last_visit(self, channel_member):
        channel_member.last_visit = timezone.now()
        channel_member.save()
