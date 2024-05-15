import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from backend.middlewares import JwtAuthMiddleware, JwtAuthMiddlewareStack
from private.routing import websocket_urlpatterns as private_urls
from group.routing import websocket_urlpatterns as group_urls
from call.routing import websocket_urlpatterns as call_urls
from channel.routing import websocket_urlpatterns as channel_urls

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AllowedHostsOriginValidator(
            JwtAuthMiddleware(
                URLRouter(private_urls + group_urls + channel_urls + call_urls)
            )
        )
    }
)
