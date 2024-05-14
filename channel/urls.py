from django.urls import path

from channel.views import ChannelCreateAPI, UserChannelMemberCreateAPI, UserChannelMemberListAPI, \
    UserChannelMemberDeleteAPI, ChannelMemberListAPI, ChannelMessageListAPI, ChannelAPI, ChannelExploreView

urlpatterns = [
    path('create/', ChannelCreateAPI.as_view(), name='create_channel'),
    path('explore/', ChannelExploreView.as_view(), name='channel_explore'),
    path('<int:channel_id>/', ChannelAPI.as_view(), name='channel'),
    path('member/create/', UserChannelMemberCreateAPI.as_view(), name='create_user_channel_member'),
    path('member/list/', UserChannelMemberListAPI.as_view(), name='user_channel_member_list'),
    path('member/<int:channel_member_id>/delete/', UserChannelMemberDeleteAPI.as_view(),
         name='delete_user_channel_member'),
    path('<int:channel_id>/member/list/', ChannelMemberListAPI.as_view(), name='channel_member_list'),
    path('<int:channel_id>/message/list/', ChannelMessageListAPI.as_view(), name='channel_message_list'),
]
