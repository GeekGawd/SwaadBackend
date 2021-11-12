from django.contrib import admin
from seller.models import Dish
from .models import Price

class PriceInlineAdmin(admin.TabularInline):
    model = Price
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [PriceInlineAdmin]


# admin.site.register( ProductAdmin)
# Dish,