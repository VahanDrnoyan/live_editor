from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from editorapp.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'editor/', ChatConsumer.as_asgi()),
]
