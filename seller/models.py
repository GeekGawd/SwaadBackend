from enum import unique
from django.db import models

# Create your models here.
from django.conf.urls import url
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import User
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.utils import timezone

Categories = (
    ('Sweets', "Sweets"), ('Rolls', 'Rolls'), ('Kebab', 'Kebab'), ('Chaat', 'Chaat'),
    ('Paneer', 'Paneer'), ('Pizza', 'Pizza'), ('Chicken', 'Chicken'), ('Healthy', 'Healthy'),
    ('Biryani', 'Biryani'), ('Shawarma', 'Shawarma'), ('Thali', 'Thali'), ('Momos', 'Momos'),
    ('Burger', 'Burger'), ('Dal', 'Dal'), ('Dosa', 'Dosa'), ('Chaap', 'Chaap'),
)

Dish_time_choices = (
    ('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'),
)

class Restaurant(models.Model):
    user = models.OneToOneField('core.User', on_delete=models.CASCADE, null=True, blank=True)
    rest_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    # logo = 

    def __str__(self):
        return self.rest_name

class Dish(models.Model):
    photo = models.ImageField(upload_to = 'img/Dish_images')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    price = models.FloatField(validators=[MinValueValidator(0)])
    title = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now_add=True)
    veg = models.BooleanField(default=True)
    category = models.CharField(choices= Categories, max_length=15)
    Dish_time = models.CharField(choices= Dish_time_choices, max_length=15, default=FileNotFoundError, null = True, blank=True)

    def __str__(self):
        return self.title

class Customer(models.Model):
    """Customer object"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    phone = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.user.get_username()

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

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,)
    # driver = models.ForeignKey(Driver, on_delete=models.CASCADE,)
    address = models.CharField(max_length=500)
    total = models.IntegerField()
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

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])

    class Meta:
        unique_together = [['user', 'dish']]
        index_together = [['user', 'dish']]
    
    def __str__(self) -> str:
        return str(f"{self.user}-->{self.dish}-->{self.stars}")




