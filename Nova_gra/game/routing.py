from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('game/<int:id>/', consumers.GameEventsConsumer),
]