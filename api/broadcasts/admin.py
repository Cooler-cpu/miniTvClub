from django.contrib import admin
from .models import LiveBroadcast, TypeBroadcast, ArchivePipelineBroadcast, Schedule

admin.site.register(TypeBroadcast)
admin.site.register(LiveBroadcast)
admin.site.register(ArchivePipelineBroadcast)
admin.site.register(Schedule)