from django.contrib import admin
from order.models import *
# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', '__str__')

admin.site.register(Order)
admin.site.register(OrderDetails)