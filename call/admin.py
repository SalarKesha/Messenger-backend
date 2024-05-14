from django.contrib.admin import register
from call.models import Call

from lib.base import BaseModelAdmin


@register(Call)
class CallAdmin(BaseModelAdmin):
    list_display = ['id', 'type', 'callee', 'caller', 'status']
