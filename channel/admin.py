from django.contrib import admin
from django.contrib.admin import register
from lib.base import BaseModelAdmin
from channel.models import Channel, ChannelMember, ChannelMessage


@register(Channel)
class ChannelAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'creator')


@register(ChannelMember)
class ChannelMemberAdmin(BaseModelAdmin):
    list_display = ('id', 'channel', 'user', 'type')


@register(ChannelMessage)
class ChannelMessageAdmin(BaseModelAdmin):
    list_display = ('id', 'channel', 'sender')
