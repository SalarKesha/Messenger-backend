from rest_framework import serializers

from account.serializers import UserSerializer
from private.models import PrivateChat, PrivateMessage


class UserPrivateChatSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    user = UserSerializer()
    owner_not_seen = serializers.IntegerField(source='get_owner_not_seen')
    user_not_seen = serializers.IntegerField(source='get_user_not_seen')
    last_message = serializers.CharField(source='get_last_private_message_content')

    class Meta:
        model = PrivateChat
        fields = ('id', 'owner', 'user', 'owner_not_seen', 'user_not_seen', 'last_message')


class PrivateChatCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateChat
        fields = ('id', 'owner', 'user')
        extra_kwargs = {
            'id': {'read_only': True},
            'owner': {'read_only': True},
        }


class PrivateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateMessage
        fields = ('id', 'type', 'sender', 'content', 'created_time')
        read_only_fields = ('id', 'created_time')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_time'] = instance.created_time.strftime("%e %B %H:%M")
        return representation


class PrivateMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateMessage
        fields = ('id', 'private_chat', 'type', 'sender', 'content', 'created_time')
        read_only_fields = ('id', 'created_time')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_time'] = instance.created_time.strftime("%e %B %H:%M")
        return representation


class PrivateChatSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    user = UserSerializer()
    owner_not_seen = serializers.IntegerField(source='get_owner_not_seen')
    user_not_seen = serializers.IntegerField(source='get_user_not_seen')

    class Meta:
        model = PrivateChat
        fields = ('id', 'owner', 'user', 'owner_not_seen', 'user_not_seen')
