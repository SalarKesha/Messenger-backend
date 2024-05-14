from django.db import models
from django.utils import timezone
from account.models import UserModel
from lib.base import BaseModel


class GroupChat(BaseModel):
    name = models.CharField(max_length=32)
    creator = models.ForeignKey(UserModel, null=True, on_delete=models.SET_NULL, related_name='groups_creator')
    image = models.ImageField(upload_to='group_chat', null=True, blank=True, default='default/group.png')

    def __str__(self):
        return f"{self.id}-group"


class GroupMember(BaseModel):
    MEMBER = 1
    ADMIN = 2
    TYPES = [
        (MEMBER, 'member'),
        (ADMIN, 'admin')
    ]
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name='group_members')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='group_members')
    type = models.PositiveSmallIntegerField(choices=TYPES, default=MEMBER)
    last_visit = models.DateTimeField(default=timezone.now)

    def get_last_message_content(self):
        group_message = GroupMessage.objects.filter(group=self.group).last()
        if group_message:
            return group_message.content
        return None

    def get_not_seen(self):
        return (GroupMessage.objects.filter(group=self.group, created_time__gt=self.last_visit)
                .exclude(sender=self).count())

    class Meta:
        unique_together = ('group', 'user')

    def __str__(self):
        return F"{self.group}-{self.user}"


class GroupMessage(BaseModel):
    MSG = 1
    JOIN = 2
    LEAVE = 3
    TYPES = [
        (MSG, 'msg'),
        (JOIN, 'join'),
        (LEAVE, 'leave'),
    ]
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name='group_messages')
    sender = models.ForeignKey(GroupMember, on_delete=models.CASCADE, related_name='group_messages')
    type = models.PositiveSmallIntegerField(choices=TYPES, default=MSG)
    content = models.TextField(max_length=100)

    def __str__(self):
        return str(self.id)
