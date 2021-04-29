from django.contrib import admin

from .models import Orders, TypePayment, StatusPayments, Payments

admin.site.register(TypePayment)
admin.site.register(StatusPayments)
admin.site.register(Payments)
admin.site.register(Orders)