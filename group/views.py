from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from group.serializers import GroupChatSerializer, UserGroupMemberSerializer, GroupMemberSerializer, \
    GroupMessageListSerializer, GroupMemberCreateSerializer, GroupChatExploreSerializer
from group.models import GroupChat, GroupMember, GroupMessage


class GroupChatCreateAPI(CreateAPIView):
    serializer_class = GroupChatSerializer
    queryset = GroupChat.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class GroupChatAPI(RetrieveAPIView):
    lookup_url_kwarg = 'group_id'
    queryset = GroupChat.objects.all()
    serializer_class = GroupChatSerializer
    permission_classes = [IsAuthenticated]


class UserGroupMemberListAPI(ListAPIView):
    serializer_class = UserGroupMemberSerializer
    queryset = GroupMember.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class GroupMemberCreateAPI(CreateAPIView):
    serializer_class = GroupMemberCreateSerializer
    queryset = GroupMember.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        group = serializer.validated_data.get('group')
        if not GroupMember.objects.filter(user=self.request.user, group=group).exists():
            serializer.save(user=self.request.user)


class GroupMemberDeleteAPI(DestroyAPIView):
    lookup_url_kwarg = 'group_member_id'
    queryset = GroupMember.objects.all()
    permission_classes = [IsAuthenticated]
    # todo: membership permission


class GroupMemberListAPI(ListAPIView):
    serializer_class = GroupMemberSerializer
    queryset = GroupMember.objects.all()
    permission_classes = [IsAuthenticated]

    # todo: membership permission
    def get_queryset(self):
        return self.queryset.filter(user=self.kwargs.get('group_id'))


class GroupMessageListAPI(ListAPIView):
    serializer_class = GroupMessageListSerializer
    queryset = GroupMessage.objects.all()
    permission_classes = [IsAuthenticated]

    # todo: membership permission
    def get_queryset(self):
        return self.queryset.filter(group=self.kwargs.get('group_id')).order_by('-created_time')


class GroupExploreAPI(ListAPIView):
    serializer_class = GroupChatExploreSerializer
    queryset = GroupChat.objects.all()
    permission_classes = [IsAuthenticated]
