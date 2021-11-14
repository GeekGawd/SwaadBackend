from os import stat, write
from django.contrib.auth import get_user_model, authenticate
from django.db.models import fields
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5,'required': True, 'error_messages': {"required": "Change this"}},
            'email': {'required': True,'error_messages': {"required": "Email field may not be blank."}},
            'name': {'required': True,'error_messages': {"required": "Name field may not be blank."}},
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


class AuthTokenSerializer(serializers.ModelSerializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField(required=True, error_messages={"required": "Email field may not be blank."})
    password = serializers.CharField(write_only=True, min_length=5)
    
    class Meta:
        model = User
        fields = ['email','tokens', 'password']

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
            return Response({'status': 'Unable to authenticate with provided credentials'}, status=status.HTTP_400_BAD_REQUEST)
        attrs['tokens'] = user.tokens
        return attrs

# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField(max_length = 255, min_length = 9)
#     password = serializers.CharField(style={'input_type': 'password'},trim_whitespace=False, write_only=True)

#     def validate(self, attrs):
#         email = attrs.get('email',)
#         password = attrs.get('password',)

#         user = authenticate(email=email, password=password)

#         if not user:
#             return Response({'status': "Unable to authenticate with provided credentials" }, status=status.HTTP_400_BAD_REQUEST)

#         return{
#             'email': user.email,
#             'tokens': user.tokens
#         }
#         return super().validate(attrs)


