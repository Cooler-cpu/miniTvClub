from django.contrib import admin

from .models import StreamsProxy


class StreamAdmin(admin.ModelAdmin):
    fields = ("name", "sourse", "fluss_pipelines", "servers_archive", "status", "data_create")

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['name']
        return self.readonly_fields

    class Media:
        js = ['/static/js/action_change.js']
      
admin.site.register(StreamsProxy, StreamAdmin)