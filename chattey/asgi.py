import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chattey.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.setup import setup
from channels.auth import AuthMiddlewareStack
from base.routing import websocket_urlpatterns

setup()

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    )
})
