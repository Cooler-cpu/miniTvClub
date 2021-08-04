from django.urls import path
from .views import Packet

urlpatterns = [
    path('getPackets',Packet.as_view()),
]