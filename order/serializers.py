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
            'address_type'
        ]

class OrderCustomerSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = ("id", "get_name", "phone", "address")

class OrderRestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("id", "phone", "address")

    def to_representation(self, instance):
        data = super(OrderRestaurantSerializer, self).to_representation(instance)
        restaurant_id = instance.id
        restaurant_name = Restaurant.objects.get(id = restaurant_id).rest_name
        data['restaurant_name'] = restaurant_name

        return data

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
        fields = ("id", "customer", "restaurant", "order_details", "total", "address", "created_at")
    
class CartSerializer(ModelSerializer):

    class Meta:
        model = CartModel
        fields = ('__all__')

class CartViewSerializer(ModelSerializer):

    order_details = OrderDetailsSerializer(many=True)
    class Meta:
        model = CartModel
        fields = ['restaurant_id', 'order_total', 'order_details']
    
    def to_representation(self, instance):
        data = super(CartViewSerializer, self).to_representation(instance)

        restaurant_name = Restaurant.objects.get(id = instance.restaurant_id).rest_name

        data['restaurant_name'] = restaurant_name

        return data
        