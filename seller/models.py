from enum import unique
import re
from django.db import models
# Create your models here.
from django.db.models import Q
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
    ('Burger', 'Burger'), ('Dal', 'Dal'), ('Dosa', 'Dosa'), ('Chaap', 'Chaap'),('Main Course', 'Main Course'),
    ('Snacks', 'Snacks'),
)

Dish_time_choices = (
    ('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'),
)

# class RestaurantQuerySet(models.QuerySet):
#     def search(self, query=None):
#         qs = self.get_queryset()
#         if query is not None:
#             or_lookup = (Q(rest_name__icontains=query) | Q(phone__icontains=query))
#             qs = qs.filter(or_lookup).distinct()
#         return qs

# class RestaurantManager(models.Manager):
#     def get_queryset(self):
#         return RestaurantQuerySet(self.model, using=self._db)
    
#     def search(self, query=None):
#         return self.get_queryset().search(query=query)

class Restaurant(models.Model):
    user = models.OneToOneField('core.User', on_delete=models.CASCADE, null=True, blank=True)
    rest_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    image = models.ImageField(upload_to = 'media/Rest_images', null = True, blank = True)
    delivery_time = models.IntegerField(default=30)
    # models.URLField(default='https://media.istockphoto.com/photos/modern-restaurant-interior-design-picture-id1211547141?k=20&m=1211547141&s=612x612&w=0&h=KiZX3NBZVCK4MlSh4BJ8hZNSJcTIMbNSSV2yusw2NmM=')
   

    # objects = RestaurantManager()
    
    def __str__(self):
        return self.rest_name

    def no_of_ratings(self):
        ratings = Rating.objects.filter(restaurant=self)
        return len(ratings)

    @property
    def avg_rating(self):
        sum = 0
        ratings = Rating.objects.filter(restaurant=self)

        if len(ratings)>0:
            for rating in ratings:
                sum += rating.stars
            return round(float(sum)/len(ratings),1)
        else:
            return 0
    
    def expense_rating(self):
        sum = 0
        dish = Dish.objects.filter(restaurant=self)
            
        if len(dish) > 0:
            for i in dish:
                sum += i.price
            avg_price = sum/len(dish)
        else:
            return 0
        
        if avg_price <= 200:
            return "$"
        
        elif 200<avg_price<=400:
            return "$$"

        else:
            return "$$$" 


class Dish(models.Model):
    # photo = models.ImageField(upload_to = 'img/Dish_images', blank = True, null = True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='rest')
    price = models.FloatField(validators=[MinValueValidator(0)])
    title = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now_add=True)
    veg = models.BooleanField(default=True)
    category = models.CharField(choices= Categories, max_length=15)
    Dish_time = models.CharField(choices= Dish_time_choices, max_length=15, default=FileNotFoundError, null = True, blank=True)
    image = models.ImageField(upload_to ='media/Dish_images', null = True, blank = True )
    # models.URLField(default='https://media.istockphoto.com/photos/food-backgrounds-table-filled-with-large-variety-of-food-picture-id1155240408?k=20&m=1155240408&s=612x612&w=0&h=Zvr3TwVQ-wlfBnvGrgJCtv-_P_LUcIK301rCygnirbk=')
    delivery_time   = models.IntegerField(default=60,blank=False)

    def __str__(self):
        return self.title
    
    def avg_rating_dish(self):
        sum = 0
        ratings = Rating.objects.filter(dish=self)
        print(ratings)
        if len(ratings)>0:
            for rating in ratings:
                sum += rating.stars
            return round(float(sum)/len(ratings),1)
        else:
            return 0

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    feedback = models.TextField()
    stars = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])

    class Meta:
        unique_together = [['user', 'dish']]
        index_together = [['user', 'dish']]
    
    def __str__(self) -> str:
        return str(f"{self.user}-->{self.restaurant}-->{self.dish}-->{self.stars}")