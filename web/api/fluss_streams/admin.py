from django.contrib import admin

from .models import Streams, Channels, Epg, Packets

from django_object_actions import DjangoObjectActions

class StreamAdmin(DjangoObjectActions, admin.ModelAdmin):
    fields = ("name", "sourse", "fluss_pipelines", "archive", "status", "data_create")

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['name']
        return self.readonly_fields

    def toolfunc(self, request, obj):
        pass
    toolfunc.label = "This will be the label of the button"  # optional
    toolfunc.short_description = "This will be the tooltip of the button"  # optional

    def make_published(modeladmin, request, queryset):
        queryset.update(status='p')

    change_actions = ('toolfunc', )
    changelist_actions = ('make_published', ) 

    class Media:
        js = ['/static/js/action_change.js']
      
admin.site.register(Streams, StreamAdmin)


from adminsortable2.admin import SortableAdminMixin
from sorl.thumbnail.admin import AdminImageMixin

class ChannelsAdmin(SortableAdminMixin, AdminImageMixin, admin.ModelAdmin):
  list_display = ("id","name", "stream")


class EpgAdmin(SortableAdminMixin, admin.ModelAdmin):
  pass


class PacketsAdmin(SortableAdminMixin, admin.ModelAdmin):
  pass

admin.site.register(Channels, ChannelsAdmin)
admin.site.register(Epg, EpgAdmin)
admin.site.register(Packets, PacketsAdmin)

