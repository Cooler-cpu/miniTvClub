from django.conf.urls import url
from django.urls.resolvers import URLPattern
from .views import SynchronizationView

urlpatterns = [
    url('synchronization', SynchronizationView.as_view())
]