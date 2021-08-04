from django.contrib import admin

import nested_admin

from .models import ServerDvr, DvrPath, Servers, AuthUrl, ServerAuth, Schedule

from fluss.service import ArchivesRequest, AuthRequest


class DvrPathInline(nested_admin.NestedTabularInline):
    model = DvrPath
    extra = 0


class ScheduleInline(nested_admin.NestedTabularInline):
    model = Schedule
    extra = 0


class ServerDvrInline(nested_admin.NestedTabularInline):
    inlines = [DvrPathInline, ScheduleInline]
    model = ServerDvr
    fields = ("name", "root", "disk_limit", "dvr_limit", "comment")
    extra = 0


class AuthUrlInline(nested_admin.NestedTabularInline):
    model = AuthUrl
    extra = 0


class ServerAuthAdmin(nested_admin.NestedModelAdmin):
    inlines = [AuthUrlInline]
    model = ServerAuth
    extra = 0
    fields = ("name", "allow_default")
    
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        auth = ServerAuth.objects.get(id=form.instance.id)
        servers = auth.servers_set.all()
        at = AuthRequest(servers)
        at.update_auths()



    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['name']
        return self.readonly_fields


class ServersAdmin(nested_admin.NestedModelAdmin):
    inlines = [ServerDvrInline]
    model = Servers
    extra = 0

    button_template = '/templates/sync_button.html'

    class Media:
        js = ['/static/js/synchronizationButton.js']



admin.site.register(Servers, ServersAdmin)
admin.site.register(ServerAuth, ServerAuthAdmin)
admin.site.register(ServerDvr)