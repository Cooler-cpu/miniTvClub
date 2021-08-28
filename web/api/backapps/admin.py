from django.contrib import admin

import nested_admin

from .models import ServerBackapps, Server


class ServerBackappsInline(nested_admin.NestedTabularInline):
    model = ServerBackapps
    extra = 0


class ServerAdmin(nested_admin.NestedModelAdmin):
    inlines = [ServerBackappsInline]
    model = Server
    extra = 0

admin.site.register(Server, ServerAdmin)
