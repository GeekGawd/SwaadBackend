from django.contrib import admin
from order.models import *
# Register your models here.

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderDetails)