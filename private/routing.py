from django.urls import path

from private.consumers import PrivateChatConsumer

websocket_urlpatterns = [
    path('private/<int:private_chat_id>/', PrivateChatConsumer.as_asgi(), name='private_chat_socket')
]
