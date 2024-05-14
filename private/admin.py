from django.contrib.admin import register
from private.models import PrivateChat, PrivateMessage
from lib.base import BaseModelAdmin
from django.contrib import admin


@register(PrivateChat)
class PrivateChatAdmin(BaseModelAdmin):
    list_display = ('id', 'owner', 'user')


@register(PrivateMessage)
class PrivateMessageAdmin(BaseModelAdmin):
    list_display = ('id', 'private_chat', 'sender')
