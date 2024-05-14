from django.urls import path

from call.consumers import GeneralCallConsumer, CallConsumer

websocket_urlpatterns = [
    path('call/', GeneralCallConsumer.as_asgi(), name='general_call_socket'),
    path('call/<int:call_id>/', CallConsumer.as_asgi(), name='call_socket'),
    # path('video-call/<int:video_chat_id>/', VideoChatConsumer.as_asgi(), name='video_call_socket'),
]
