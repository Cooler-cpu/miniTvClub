from django.contrib import admin

import nested_admin

from .models import ServerBackapps, Server

from django_admin_row_actions import AdminRowActionsMixin


class ServerBackappsInline(AdminRowActionsMixin, nested_admin.NestedTabularInline):
    model = ServerBackapps
    extra = 0


class ServerAdmin(AdminRowActionsMixin, nested_admin.NestedModelAdmin):
    # change_form_template = 'admin/fluss_servers/model/change_form.html'
    
    inlines = [ServerBackappsInline]
    model = Server
    extra = 0

    def get_row_actions(self, obj):
        row_actions = [
            {
                'label': 'Edit',
                'url': obj.get_absolute_url(),
            }
        ]
        row_actions += super(ServerAdmin, self).get_row_actions(obj)
        return row_actions
        

admin.site.register(Server, ServerAdmin)
