from django.contrib import admin
from .models import Channels, Epg, Packets

from adminsortable2.admin import SortableAdminMixin


class ChannelsAdmin(SortableAdminMixin, admin.ModelAdmin):
  pass

class EpgAdmin(SortableAdminMixin, admin.ModelAdmin):
  pass

class PacketsAdmin(SortableAdminMixin, admin.ModelAdmin):
  pass


admin.site.register(Channels, ChannelsAdmin)
admin.site.register(Epg, EpgAdmin)
admin.site.register(Packets, PacketsAdmin)
