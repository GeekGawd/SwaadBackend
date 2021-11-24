from django.db.models import fields
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import *
from seller.models import Restaurant, Dish
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

    def to_representation(self, instance):
        data = super(OrderDetailsSerializer, self).to_representation(instance)
        dish_id = instance.id
        dish_name = Dish.objects.get(id = dish_id).title
        data['dish_name'] = dish_name

        return data
         
class OrderSerializer(ModelSerializer):
    customer = OrderCustomerSerializer()
    restaurant = OrderRestaurantSerializer()
    order_details = OrderDetailsSerializer(many = True)

    class Meta:
        model = Order
        fields = ("id", "customer", "restaurant", "order_details", "total", "address")
    
class CartSerializer(ModelSerializer):

    class Meta:
        model = CartModel
        fields = ('__all__')