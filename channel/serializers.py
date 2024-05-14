from account.serializers import UserSerializer
from channel.models import Channel, ChannelMember, ChannelMessage
from rest_framework import serializers


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'creator', 'name', 'image')
        extra_kwargs = {
            'id': {'read_only': True},
            'creator': {'read_only': True}
        }


class ChannelExploreSerializer(serializers.ModelSerializer):
    joined = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = ('id', 'creator', 'name', 'image', 'joined')
        extra_kwargs = {
            'id': {'read_only': True},
            'creator': {'read_only': True}
        }

    def get_joined(self, obj):
        request = self.context.get('request')
        if ChannelMember.objects.filter(channel=obj, user=request.user).exists():
            return True
        return False


class ChannelMemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelMember
        fields = ('id', 'channel',)
        extra_kwargs = {
            'id': {'read_only': True},
        }


class UserChannelMemberSerializer(serializers.ModelSerializer):
    # list user channel member
    channel = ChannelSerializer()
    not_seen = serializers.IntegerField(source='get_not_seen')
    last_message = serializers.CharField(source='get_last_message_content')

    class Meta:
        model = ChannelMember
        fields = ('id', 'channel', 'not_seen', 'last_message')
        extra_kwargs = {
            'id': {'read_only': True},
            'not_seen': {'read_only': True},
        }


class ChannelMemberListSerializer(serializers.ModelSerializer):
    # list a channel members
    user = UserSerializer()

    class Meta:
        model = ChannelMember
        fields = ('id', 'user', 'type')
        extra_kwargs = {
            'id': {'read_only': True}
        }


# class ChannelMemberDeleteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ChannelMember
#         fields = ('id', 'channel')
#         extra_kwargs = {
#             'id': {'read_only': True}
#         }


class ChannelMessageListSerializer(serializers.ModelSerializer):
    sender = ChannelMemberListSerializer()

    class Meta:
        model = ChannelMessage
        fields = ('id', 'sender', 'content', 'created_time')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_time'] = instance.created_time.strftime("%e %B %H:%M")
        return representation


class ChannelMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelMessage
        fields = ('channel', 'sender', 'content')
