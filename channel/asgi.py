"""
ASGI config for channel project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from chat.middleware import QueryAuthMiddleware
from chat.routing import websocket_urlpatterns as chat_routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'channel.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # Just HTTP for now. (We can add other protocols later.)
    "websocket":
        AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                QueryAuthMiddleware(
                    URLRouter(chat_routing)
                )
            )
        ),
})
