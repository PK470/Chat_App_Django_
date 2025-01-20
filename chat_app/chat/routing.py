from django.urls import path
from . import consumer

websocket_urlpatterns = [
    path('ws/chat/<str:receiver>/', consumer.ChatConsumer.as_asgi())

]