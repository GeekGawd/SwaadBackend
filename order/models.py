from django.db import models
from django.db.models.fields import IntegerField
from django.db.models.fields.related import OneToOneField
from django.utils import timezone, tree
from django_filters.utils import try_dbfield
from rest_framework import serializers
from core.models import User
from seller.models import Dish
# Create your models here.

ADDRESS_TYPE = (
    ('Home', 'Home'), ("Work", 'Work'),
)

class Customer(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='customer', null=True)
    address_type = models.CharField(choices=ADDRESS_TYPE, max_length=4, default="Home")
    phone = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.user.get_username()} --> {self.address}"
    
    def get_name(self):
        return self.user.name

class Order(models.Model):
    # COOKING = 1
    # READY = 2
    # ONTHEWAY = 3
    # DELIVERED = 4

    # STATUS_CHOICES = (
    #     (COOKING, "Cooking"),
    #     (READY, "Ready"),
    #     (ONTHEWAY, "On the way"),
    #     (DELIVERED, "Delivered"),
    # )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,)
    restaurant = models.ForeignKey('seller.Restaurant', on_delete=models.CASCADE,)
    total = models.IntegerField()
    address = models.CharField(max_length=250, null=True)
    # is_paid = models.BooleanField(default=False)
    # status = models.IntegerField(choices = STATUS_CHOICES)
    created_at = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return str(self.id)


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details', null=True)
    # cart_details = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_details')
    dish = models.ForeignKey('seller.Dish', on_delete=models.CASCADE,)
    quantity = models.IntegerField()
    sub_total = models.IntegerField()
    ordered = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.id)


class CartModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    # dish = models.ManyToManyField(Dish)
    order_details = models.ManyToManyField(OrderDetails)
    restaurant_id = models.IntegerField()
    order_total = models.IntegerField(default=0)

    def __str__(self):
        return self.user.email
    
    def total(self):
        
        total = (self.order_total * 18)/100
        

# class CartDetail(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     amount = models.IntegerField(blank=True, null=True)

#     def __str__(self):
#         return self.user.name