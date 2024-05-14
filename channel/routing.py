from django.urls import path

from channel.consumers import ChannelConsumer

websocket_urlpatterns = [
    path('channel/<channel_id>/', ChannelConsumer.as_asgi(), name='channel_chat')
]
