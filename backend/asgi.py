"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from private.routing import websocket_urlpatterns as private_urls
from group.routing import websocket_urlpatterns as group_urls
from channel.routing import websocket_urlpatterns as channel_urls
from call.routing import websocket_urlpatterns as call_urls
from django.core.asgi import get_asgi_application
from backend.middlewares import JwtAuthMiddleware, JwtAuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AllowedHostsOriginValidator(
            JwtAuthMiddleware(URLRouter(private_urls + group_urls + channel_urls + call_urls))
        )
    }
)
