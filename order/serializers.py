from django.db.models import fields
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, authenticate

class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id',
            'user',
            'phone',
            'address',
        ]

class OrderCustomerSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = ("id", "get_name", "phone", "address")

class OrderRestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("id", "phone", "address")

class OrderMealSerializer(ModelSerializer):
    class Meta:
        model = Dish
        fields = ("id", "price")

class OrderDetailsSerializer(ModelSerializer):
    dish = OrderMealSerializer()

    class Meta:
        model = OrderDetails
        fields = ("id", "dish", "quantity", "sub_total")

class OrderSerializer(ModelSerializer):
    customer = OrderCustomerSerializer()
    restaurant = OrderRestaurantSerializer()
    order_details = OrderDetailsSerializer(many = True)

    class Meta:
        model = Order
        fields = ("id", "customer", "restaurant", "order_details", "total", "address")