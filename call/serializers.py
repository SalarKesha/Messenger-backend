from rest_framework import serializers

from account.serializers import UserSerializer
from call.models import Call


class CallSerializer(serializers.ModelSerializer):
    caller = UserSerializer()
    callee = UserSerializer()

    class Meta:
        model = Call
        fields = ('id', 'private_chat', 'type', 'caller', 'callee', 'status', 'created_time')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_time'] = instance.created_time.strftime("%a %e %B %H:%M")
        return representation