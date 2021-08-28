from django.conf.urls import url
from django.urls.resolvers import URLPattern
from .views import BackappsServerActivate

urlpatterns = [
    url('activate', BackappsServerActivate.as_view()), 
]