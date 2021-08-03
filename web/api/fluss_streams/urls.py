from django.urls import path

from .views import GetPipelinesListView


urlpatterns = [
    path("api/v1/get_piplines", GetPipelinesListView.as_view()),
]