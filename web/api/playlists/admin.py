from django.contrib import admin

from .models import Playlists, Ips

admin.site.register(Ips)
# admin.site.register(Packets)
admin.site.register(Playlists)
