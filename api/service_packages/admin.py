from django.contrib import admin

from .models import Package, TypePackage

admin.site.register(Package)
admin.site.register(TypePackage)