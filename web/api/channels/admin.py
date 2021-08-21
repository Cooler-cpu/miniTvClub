from django.contrib import admin
from django.utils.html import format_html
from .models import Channels, Epg, Packets

from adminsortable2.admin import SortableAdminMixin


class ChannelsAdmin(SortableAdminMixin, admin.ModelAdmin):
  list_display = ("id","name", "stream")
  readonly_fields = ('preview',)
  
  def preview(self, obj):
    return format_html('<img src="{}" width="{}" style="object-fit: contain;">'.format(obj.logo.url, "150px"))
  
  preview.short_description = 'Превью'
  preview.allow_tags = True


class EpgAdmin(SortableAdminMixin, admin.ModelAdmin):
  pass


class PacketsAdmin(SortableAdminMixin, admin.ModelAdmin):
  pass


admin.site.register(Channels, ChannelsAdmin)
admin.site.register(Epg, EpgAdmin)
admin.site.register(Packets, PacketsAdmin)
