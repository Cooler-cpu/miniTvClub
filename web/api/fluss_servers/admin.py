from django.contrib import admin
from django.db import models

from .models import ServerDvr, DvrPath, Servers, AuthUrl, ServerAuth, Schedule

import nested_admin


class DvrPathInline(nested_admin.NestedTabularInline):
    model = DvrPath
    extra = 0


class ScheduleInline(nested_admin.NestedTabularInline):
    model = Schedule
    extra = 0


class ServerDvrInline(nested_admin.NestedTabularInline):
    inlines = [DvrPathInline, ScheduleInline]
    model = ServerDvr
    extra = 0


class ServerAdmin(nested_admin.NestedModelAdmin):
    inlines = [ServerDvrInline]
    model = Servers
    extra = 0


class AuthUrlInline(nested_admin.NestedTabularInline):
    model = AuthUrl
    extra = 0


class ServerAuthAdmin(nested_admin.NestedModelAdmin):
    inlines = [AuthUrlInline]
    model = ServerAuth
    extra = 0


admin.site.register(Servers, ServerAdmin)
admin.site.register(ServerAuth, ServerAuthAdmin)