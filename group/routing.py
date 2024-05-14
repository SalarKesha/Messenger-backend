from django.urls import path
from group.consumers import GroupChatConsumer

websocket_urlpatterns = [
    path('group/<int:group_chat_id>/', GroupChatConsumer.as_asgi(), name='group_chat_socket')
]
