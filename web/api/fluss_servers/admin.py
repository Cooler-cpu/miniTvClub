from django.contrib import admin
from django.db import models
from django.db.models import fields

from .models import ServerDvr, DvrPath, Servers, AuthUrl, ServerAuth, Schedule

import nested_admin


class DvrPathInline(nested_admin.NestedTabularInline):
    model = DvrPath
    extra = 0


class ScheduleInline(nested_admin.NestedTabularInline):
    model = Schedule
    extra = 0


class ServerDvrInline(nested_admin.NestedModelAdmin):
    inlines = [DvrPathInline, ScheduleInline]
    model = ServerDvr
    fields = ("name", "root", "disk_limit", "dvr_limit", "comment")

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['name']
        return self.readonly_fields


class AuthUrlInline(nested_admin.NestedTabularInline):
    model = AuthUrl
    extra = 0


class ServerAuthAdmin(nested_admin.NestedModelAdmin):
    inlines = [AuthUrlInline]
    model = ServerAuth
    extra = 0


admin.site.register(Servers)
admin.site.register(ServerAuth, ServerAuthAdmin)
admin.site.register(ServerDvr, ServerDvrInline)