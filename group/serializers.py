from rest_framework import serializers

from account.serializers import UserSerializer
from group.models import GroupChat, GroupMember, GroupMessage


class GroupChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChat
        fields = ('id', 'name', 'image')
        extra_kwargs = {
            'id': {'read_only': True}
        }


class GroupChatExploreSerializer(serializers.ModelSerializer):
    joined = serializers.SerializerMethodField()

    class Meta:
        model = GroupChat
        fields = ('id', 'name', 'image', 'joined')
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def get_joined(self, obj):
        request = self.context.get('request')
        if GroupMember.objects.filter(group=obj, user=request.user).exists():
            return True
        return False


class UserGroupMemberSerializer(serializers.ModelSerializer):
    group = GroupChatSerializer()
    not_seen = serializers.IntegerField(source='get_not_seen')
    last_message = serializers.CharField(source='get_last_message_content')

    class Meta:
        model = GroupMember
        fields = ('id', 'group', 'not_seen', 'last_message')


class GroupMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = GroupMember
        fields = ('id', 'user', 'type')


class GroupMemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = ('id', 'group', 'user')
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
        }


class GroupMessageListSerializer(serializers.ModelSerializer):
    sender = GroupMemberSerializer()

    class Meta:
        model = GroupMessage
        fields = ('id', 'sender', 'type', 'content', 'created_time')
        extra_kwargs = {
            'id': {'read_only': True},
            'created_time': {'read_only': True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_time'] = instance.created_time.strftime("%e %B %H:%M")
        return representation


class GroupMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMessage
        fields = ('group', 'sender', 'type', 'content')
