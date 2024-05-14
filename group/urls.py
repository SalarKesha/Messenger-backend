from django.urls import path

from group.views import GroupChatCreateAPI, UserGroupMemberListAPI, GroupMemberListAPI, GroupMessageListAPI, \
    GroupMemberCreateAPI, GroupMemberDeleteAPI, GroupChatAPI, GroupExploreAPI

urlpatterns = [
    path('create/', GroupChatCreateAPI.as_view(), name='create_group_chat'),
    path('explore/', GroupExploreAPI.as_view(), name='group_explore'),
    path('<int:group_id>/', GroupChatAPI.as_view(), name='group_chat'),
    path('member/list/', UserGroupMemberListAPI.as_view(), name='user_group_member_list'),
    path('member/create/', GroupMemberCreateAPI.as_view(), name='create_group_member'),
    path('member/<int:group_member_id>/delete/', GroupMemberDeleteAPI.as_view(), name='delete_group_member'),
    path('<int:group_id>/member/list/', GroupMemberListAPI.as_view(), name='group_member_list'),
    path('<int:group_id>/message/list/', GroupMessageListAPI.as_view(), name='group_message_list'),
]
