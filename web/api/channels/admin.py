from django.contrib import admin
from .models import Channels, Epg

from adminsortable2.admin import SortableAdminMixin


class ChannelsAdmin(SortableAdminMixin, admin.ModelAdmin):
  pass

class EpgAdmin(SortableAdminMixin, admin.ModelAdmin):
  pass

admin.site.register(Channels, ChannelsAdmin)
admin.site.register(Epg, EpgAdmin)
# Register your models here.
