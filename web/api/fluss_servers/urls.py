from django.conf.urls import url
from django.urls.resolvers import URLPattern
from .views import ModelSynchronizationView, MediaSynchronizationView

urlpatterns = [
    url('synchronizationModel',ModelSynchronizationView.as_view()),
    url('synchronizationMedia',MediaSynchronizationView.as_view())
]