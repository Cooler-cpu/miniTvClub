from django.contrib import admin

from .models import PacketOrder

class PacketOrderAdmin(admin.ModelAdmin):
    fields = ("order_type", "user", "creator", "status", "packet", "price", "date", "dateStop", "period", "comment")

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['period','dateStop']
        return self.readonly_fields
        

admin.site.register(PacketOrder, PacketOrderAdmin)
