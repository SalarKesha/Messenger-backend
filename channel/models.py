from django.db import models
from django.db.models import Count
from django.utils import timezone

from account.models import UserModel
from lib.base import BaseModel


class Channel(BaseModel):
    name = models.CharField(max_length=32)
    creator = models.ForeignKey(UserModel, null=True, on_delete=models.SET_NULL, related_name='channels')
    image = models.ImageField(upload_to='channel', null=True, blank=True, default='default/channel.png')

    def __str__(self):
        return f"{self.id}-channel"


class ChannelMember(BaseModel):
    MEMBER = 1
    ADMIN = 2
    TYPES = (
        (MEMBER, 'member'),
        (ADMIN, 'admin')
    )
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='channel_members')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='channel_members')
    type = models.PositiveSmallIntegerField(choices=TYPES, default=MEMBER)
    last_visit = models.DateTimeField(default=timezone.now)

    def get_last_message_content(self):
        channel_message = ChannelMessage.objects.filter(channel=self.channel).last()
        if channel_message:
            return channel_message.content
        return None

    def get_not_seen(self):
        return ChannelMessage.objects.filter(sender=self, created_time__gt=self.last_visit).exclude(sender=self).count()

    class Meta:
        unique_together = ('channel', 'user')

    def __str__(self):
        return f"{self.channel}-{self.user}"


class ChannelMessage(BaseModel):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='channel_messages')
    sender = models.ForeignKey(ChannelMember, on_delete=models.CASCADE, related_name='channel_messages')
    content = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.channel}-{self.sender}"
