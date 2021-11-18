from django.db.models.base import Model
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import *
from django.contrib.auth import get_user_model, authenticate
from django.db.models import fields
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from django_filters import FilterSet, ChoiceFilter

# class CategorySerializer(ModelSerializer):
#     photo = SerializerMethodField()


#     def get_photo(self, obj):
#         try:
#             return obj.food.first().photo
#         except:
#             return ""

#     class Meta:
#         model = Category
#         fields = [
#             'id',
#             'name',
#             'photo',
#         ]

class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'id',
            'user',
            'image',
            'rest_name',
            'phone',
            'address',
            'no_of_ratings',
            'avg_rating',
        ]

class DishSerializer(ModelSerializer):
    class Meta:
        model = Dish
        fields = [
            'id',
            'image',
            'title',
            'price',
            'category',
            'veg',
            'restaurant',
        ]

class AllInfoSerializer(ModelSerializer):
    # category = CategorySerializer
    restaurant = RestaurantSerializer

    class Meta:
        model = Dish
        fields = [
            'id',
            'image',
            'title',
            'price',
            'category',
            'restaurant',
        ]


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5,'required': True, 'error_messages': {"required": "Change this"}},
            'email': {'required': True,'error_messages': {"required": "Email field may not be blank."}},
            'name': {'required': True,'error_messages': {"required": "Email field may not be blank."}},
            }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField(required=True, error_messages={"required": "Email field may not be blank."})
    password = serializers.CharField(
        style={'input_type': 'password'},
        required=True, 
        error_messages={"required": "Email field may not be blank."},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs

class DishSerializer(ModelSerializer):
    # image = serializers.SerializerMethodField()

    # def get_image(self, dish):
    #     request = self.context.get('request')
    #     image_url = dish.image.url
    #     return request.build_absolute_uri(image_url)

    class Meta:
        model = Dish
        fields = ("id", "title", "image", "price", "veg","category")

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('__all__')
        
class CategoryFilter(FilterSet):

    Categories = ChoiceFilter(choices=Dish.category)

    class Meta:
        model = Dish
        fields = ('Categories', )