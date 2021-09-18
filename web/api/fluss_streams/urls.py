from typing import Text
from django.urls import path

from .views import GetPipelinesListView
from .views import Packet


urlpatterns = [
    path('v1/get_piplines', GetPipelinesListView.as_view()),
    path('getPackets', Packet.as_view())
]



