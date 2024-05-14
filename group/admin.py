from django.contrib.admin import register
from group.models import GroupChat, GroupMember, GroupMessage
from lib.base import BaseModelAdmin


@register(GroupChat)
class GroupAdmin(BaseModelAdmin):
    list_display = ('id', 'creator')


@register(GroupMember)
class GroupMemberAdmin(BaseModelAdmin):
    list_display = ('id', 'group', 'user', 'type')


@register(GroupMessage)
class GroupMessageAdmin(BaseModelAdmin):
    list_display = ('id', 'group', 'sender')
