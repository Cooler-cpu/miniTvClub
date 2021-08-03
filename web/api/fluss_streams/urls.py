from typing import Text
from django.urls import path

from .views import GetPipelinesListView
from .views import Test

urlpatterns = [
    path("api/v1/get_piplines", GetPipelinesListView.as_view()),
    path("la", Test.as_view())
]



