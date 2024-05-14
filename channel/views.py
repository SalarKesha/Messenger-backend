from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListCreateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from channel.serializers import ChannelSerializer, UserChannelMemberSerializer, ChannelMemberListSerializer, \
    ChannelMemberCreateSerializer, ChannelMessageListSerializer, ChannelExploreSerializer
from channel.models import Channel, ChannelMessage, ChannelMember
from lib.permissions import UserChannelMemberOwnership


class ChannelCreateAPI(CreateAPIView):
    serializer_class = ChannelSerializer
    queryset = Channel.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(creator=self.request.user)


class ChannelAPI(RetrieveAPIView):
    serializer_class = ChannelSerializer
    lookup_url_kwarg = 'channel_id'
    queryset = Channel.objects.all()
    permission_classes = [IsAuthenticated]


class UserChannelMemberCreateAPI(CreateAPIView):
    serializer_class = ChannelMemberCreateSerializer
    queryset = ChannelMember.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        channel = serializer.validated_data.get('channel')
        if not ChannelMember.objects.filter(channel=channel, user=self.request.user).exists():
            serializer.save(user=self.request.user)


class UserChannelMemberListAPI(ListAPIView):
    serializer_class = UserChannelMemberSerializer
    queryset = ChannelMember.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class UserChannelMemberDeleteAPI(DestroyAPIView):
    queryset = ChannelMember.objects.all()
    lookup_url_kwarg = 'channel_member_id'
    permission_classes = [IsAuthenticated, UserChannelMemberOwnership]


class ChannelMemberListAPI(ListAPIView):
    serializer_class = ChannelMemberListSerializer
    queryset = ChannelMember.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(channel=self.kwargs.get('channel_id'))


class ChannelMessageListAPI(ListAPIView):
    serializer_class = ChannelMessageListSerializer
    queryset = ChannelMessage.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(channel=self.kwargs.get('channel_id')).order_by('-created_time')


class ChannelExploreView(ListAPIView):
    serializer_class = ChannelExploreSerializer
    queryset = Channel.objects.all()
    permission_classes = [IsAuthenticated]
