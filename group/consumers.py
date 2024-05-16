from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.utils import timezone

from group.models import GroupChat, GroupMember, GroupMessage
from group.serializers import GroupMessageListSerializer, GroupMessageSerializer


class GroupChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get('user')
        self.group_chat_id = self.scope.get('url_route').get('kwargs').get('group_chat_id')
        self.chat_room_id = f"gc_{self.group_chat_id}"
        if not self.user.is_authenticated:
            await self.close()
            return
        self.group_member = await self.get_group_member(self.user)
        if self.group_member:
            await self.update_last_visit(self.group_member)
            await self.channel_layer.group_add(self.chat_room_id, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, code):
        await self.update_last_visit(self.group_member)
        await self.channel_layer.group_discard(self.chat_room_id, self.channel_name)

    async def receive_json(self, content, **kwargs):
        # group_message = await self.save_group_message(
        #     sender=self.group_member, message_type=content.get('message_type'), text=content.get('text'))
        group_message = await self.save_group_message(content=content, sender=self.group_member)
        if group_message:
            await self.channel_layer.group_send(
                self.chat_room_id,
                {'type': 'send_group_message', 'group_message': group_message}
            )

    async def send_group_message(self, event):
        await self.send_json(content={'message': event.get('group_message')})

    @database_sync_to_async
    def get_group_member(self, user):
        return GroupMember.objects.filter(group_id=self.group_chat_id, user=user).first()

    @database_sync_to_async
    def save_group_message(self, content, sender):
        data = {
            'group': sender.group.id,
            'sender': sender.id,
            'type': content.get('message_type'),
            'content': content.get('text')
        }
        serializer = GroupMessageSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            serializer_data = GroupMessageListSerializer(instance).data
            return serializer_data
        return False

    @database_sync_to_async
    def update_last_visit(self, group_member):
        group_member.last_visit = timezone.now()
        group_member.save()
