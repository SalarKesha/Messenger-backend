from rest_framework.permissions import BasePermission

from channel.models import ChannelMember


class UserChannelMemberOwnership(BasePermission):
    def has_permission(self, request, view):
        channel_member = ChannelMember.objects.filter(id=view.kwargs.get('channel_member_id')).first()
        if channel_member:
            return channel_member.user == request.user
        return False
