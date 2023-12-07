from django.urls import re_path

from . import services

websocket_urlpatterns = [
    re_path(r"ws/text_chat/(?P<id>\w+)/$",
            services.ChatConsumer.as_asgi()),
]
