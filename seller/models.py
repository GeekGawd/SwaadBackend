from django.db import models

# Create your models here.
from django.conf.urls import url
from django.db import models
from django.core.validators import MinValueValidator
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

Meal_time_choices = (
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
    photo = models.ImageField(upload_to = 'img/meal_images')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    price = models.FloatField(validators=[MinValueValidator(0)])
    title = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now_add=True)
    veg = models.BooleanField(default=True)
    category = models.CharField(choices= Categories, max_length=15)
    meal_time = models.CharField(choices= Meal_time_choices, max_length=15, default=FileNotFoundError)

    def __str__(self):
        return self.title



