from django.db import models
from django.utils import timezone, tree
from rest_framework import serializers
from seller.models import Restaurant, Dish
from core.models import User
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField('core.User', on_delete=models.CASCADE, related_name='customer')
    phone = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.user.get_username()
    
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
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,)
    total = models.IntegerField()
    address = models.CharField(max_length=250, null=True)
    # status = models.IntegerField(choices = STATUS_CHOICES)
    created_at = models.DateTimeField(default = timezone.now)
    # picked_at = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return str(self.id)

class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE,)
    quantity = models.IntegerField()
    sub_total = models.IntegerField()


    def __str__(self):
        return str(self.id)

class CartModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dish = models.ManyToManyField(Dish)

    def __str__(self):
        return f"Cart of {self.user}"