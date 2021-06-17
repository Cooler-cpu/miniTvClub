from django.contrib import admin
from .models import Streams

class StreamAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['name']
        return self.readonly_fields
      
admin.site.register(Streams, StreamAdmin)
