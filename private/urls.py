from django.urls import path
from private.views import UserPrivateChatAPI, PrivateMessageListAPI, PrivateChatAPI, PrivateChatCreateAPI

urlpatterns = [
    path('list/', UserPrivateChatAPI.as_view(), name='private_chat_list'),
    path('<int:private_chat_id>/', PrivateChatAPI.as_view(), name='private_chat'),
    path('create/', PrivateChatCreateAPI.as_view(), name='create_private_chat'),
    path('<int:private_chat_id>/message/list/', PrivateMessageListAPI.as_view(), name='private_message_list')
]
