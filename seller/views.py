from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from core.models import User
from .models import *
from .serializers import *
from rest_framework import generics, status, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from core.models import *
from user.serializers import UserSerializer, AuthTokenSerializer
from django.core.mail import send_mail, EmailMessage
import random, time, datetime
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

# class CategoryViewSet(viewsets.ModelViewSet):
#     serializer_class = CategorySerializer
#     queryset = Category.objects.all()

class RestaurantViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()

class CreateSellerView(APIView):
    """Create a new user in the system"""

    def post(self, request):
        data = request.data
        serializer1 = UserSerializer(data = data)
        if serializer1.is_valid():
            user = serializer1.save()
        
        id1 = user.id
        # try:
        #     user = User.objects.filter(id=id1)[0]
        # except:
        #     raise Http404

        data['user'] = id1
        serializer2 = RestaurantSerializer(data = data)
        # if Restaurant.objects.all().filter(user=id1) is None:
        if serializer2.is_valid():
            serializer2.save()
            return Response(serializer2.data, status=status.HTTP_201_CREATED)
        return Response(data={'details':'User already have a restaurant.'},status=status.HTTP_400_BAD_REQUEST)

class LoginView(ObtainAuthToken):
    """Create a new auth token for user"""
    # serializer_class = AuthTokenSerializer
    # renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    def post(self, request, *args, **kwargs):
        request_email = request.data.get('email',)
        try:
            user1 = User.objects.get(email__iexact = request_email)
        except:
            return Response({
                'detail':'User not registered'
            })
        if user1.is_active is True:
            serializer = AuthTokenSerializer(data=request.data, context={'request':request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token':token.key
            })
        else:
            return Response({
                'detail':'User is not validated please got to ligin otp first'
            })

def customer_get_restaurants(request):
    restaurants = RestaurantSerializer(
        Restaurant.objects.all().order_by("-id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"restaurants": restaurants})