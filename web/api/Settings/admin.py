from django.contrib import admin

from .models import Settings, Language

admin.site.register(Language)
admin.site.register(Settings)
