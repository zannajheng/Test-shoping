from django.urls import path, re_path
from apps.service import consumers

websocket_urlpatterns = [
    re_path(r'room/(?P<group>\w+)/$', consumers.ChatConsumer.as_asgi()),

]