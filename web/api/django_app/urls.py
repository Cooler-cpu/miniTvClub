from django import urls
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import Load

from django.conf.urls import include, url

urlpatterns = [
    path('server/', include('fluss_servers.urls')),
    path('backapps/', include('backapps.urls')),
    path('grappelli/', include('grappelli.urls')),
    path('_nested_admin/', include('nested_admin.urls')),
    path('admin/', admin.site.urls),
    path('test', Load.as_view()),
    path('api/user/', include('users.urls')),
    # path('api/', include('channels.urls')),
    path('api/', include('fluss_streams.urls')),
    # path('', include('auth.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
