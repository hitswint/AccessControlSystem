# import os
# from channels.asgi import get_channel_layer

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AccessControlSystem.settings")

# channel_layer = get_channel_layer()
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import AC.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AccessControlSystem.settings")

application = ProtocolTypeRouter({
    # http请求使用这个
    "http": get_asgi_application(),

    # websocket请求使用这个
    "websocket": AuthMiddlewareStack(
        URLRouter(
            AC.routing.websocket_urlpatterns
        )
    ),
})
