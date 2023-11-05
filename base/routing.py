import django
from django.urls import path, re_path
from .consumers import PrivateChatConsumer, GroupChatConsumer

django.setup()

websocket_urlpatterns = [
    path('wss/private-chat/<str:username>/', PrivateChatConsumer.as_asgi()),
    path('wss/group-chat/<int:id>/', GroupChatConsumer.as_asgi()),
]