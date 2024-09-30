# routing.py
from django.urls import path
from .consumers import MachineConsumer

websocket_urlpatterns = [
    path('ws/machines/', MachineConsumer.as_asgi()),
]