from django.db import models
from account.models import UserModel
from lib.base import BaseModel

from datetime import datetime
from django.utils import timezone


class PrivateChat(BaseModel):
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='private_chats_owner')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='private_chats_user')
    owner_last_visit = models.DateTimeField(default=timezone.now)
    user_last_visit = models.DateTimeField(default=timezone.now)

    def get_last_private_message_content(self):
        private_message = PrivateMessage.objects.filter(private_chat=self).last()
        if private_message:
            return private_message.content
        return None

    def get_owner_not_seen(self):
        return PrivateMessage.objects.filter(private_chat=self, created_time__gt=self.owner_last_visit).exclude(
            sender=self.owner).count()

    def get_user_not_seen(self):
        return PrivateMessage.objects.filter(private_chat=self, created_time__gt=self.user_last_visit).exclude(
            sender=self.user).count()

    def __str__(self):
        return f"{self.owner}-{self.user}"


class PrivateMessage(BaseModel):
    MSG = 1
    AUDIO_CALL = 2
    VIDEO_CALL = 3
    TYPES = [
        (MSG, 'message'),
        (AUDIO_CALL, 'audio call'),
        (VIDEO_CALL, 'video call'),
    ]
    type = models.PositiveSmallIntegerField(choices=TYPES, default=MSG)
    private_chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE, related_name='private_messages')
    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='private_messages')
    content = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.private_chat}-{self.sender}"
