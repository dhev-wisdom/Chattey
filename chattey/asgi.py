# isort: skip_file
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

import os
import django

django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from base.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chattey.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"



application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    )
})
