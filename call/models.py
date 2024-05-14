from account.models import UserModel
from lib.base import BaseModel
from django.db import models

from private.models import PrivateChat


class Call(BaseModel):
    VIDEO = 1
    AUDIO = 2
    TYPES = [
        (VIDEO, 'video'),
        (AUDIO, 'audio')
    ]
    NOT_ANSWERED = 1
    ANSWERED = 2
    CANCELED = 3
    REJECT = 4
    STATUS = [
        (NOT_ANSWERED, 'not_answered'),
        (ANSWERED, 'answered'),
        (CANCELED, 'canceled'),
        (REJECT, 'reject')
    ]
    private_chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE, related_name='calls')
    type = models.PositiveSmallIntegerField(choices=TYPES, default=VIDEO)
    caller = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='calls_caller')
    callee = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='calls_callee')
    status = models.PositiveSmallIntegerField(choices=STATUS, default=NOT_ANSWERED)

    def __str__(self):
        return str(self.id)
