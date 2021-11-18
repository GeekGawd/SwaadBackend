from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
# Register your models here.

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'title', 'restaurant')

admin.site.register(Rating)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'rest_name', 'phone', 'address')