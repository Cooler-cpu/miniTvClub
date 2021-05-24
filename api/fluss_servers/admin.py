from django.contrib import admin
from django.db import models

from .models import ServerDvr, DvrPath, Servers, AuthUrl, ServerAuth

import nested_admin


class AuthUrlInline(nested_admin.NestedTabularInline):
    model = AuthUrl
    extra = 1


class ServerAuthAdmin(nested_admin.NestedTabularInline):
    inlines = [AuthUrlInline]
    model = ServerAuth
    extra = 1


class DvrPathInline(nested_admin.NestedTabularInline):
    model = DvrPath
    extra = 1


class ServerDvrInline(nested_admin.NestedTabularInline):
    inlines = [DvrPathInline]
    model = ServerDvr
    extra = 1


class ServerAdmin(nested_admin.NestedModelAdmin):
    inlines = [ServerDvrInline, ServerAuthAdmin]
    model = Servers
    extra = 1


admin.site.register(Servers, ServerAdmin)