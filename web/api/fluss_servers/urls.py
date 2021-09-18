from django.conf.urls import url
from django.urls.resolvers import URLPattern
from .views import ModelSynchronizationView, MediaSynchronizationView, ServerAction

from django.urls import path

urlpatterns = [
    url('synchronizationModel',ModelSynchronizationView.as_view()),
    url('synchronizationMedia',MediaSynchronizationView.as_view()),
    path('server_action/<int:pk>/', ServerAction.as_view(), name='server_action')
]