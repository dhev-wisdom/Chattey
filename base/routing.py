from django.urls import path, re_path
from .consumers import PrivateChatConsumer, GroupChatConsumer

websocket_urlpatterns = [
    path('ws/private-chat/<str:username>/', PrivateChatConsumer.as_asgi()),
    path('ws/group-chat/<int:id>/', GroupChatConsumer.as_asgi()),
    # re_path(r"ws/private-chat/(P<user_id>\d+)/$", PrivateChatConsumer.as_asgi()),
    # re_path(r"ws/group-chat/(P<group_id>\d+)/$", GroupChatConsumer.as_asgi())
]