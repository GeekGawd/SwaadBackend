from rest_framework import generics, serializers, status, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from core.models import *
from order.models import *
from order.serializers import CustomerSerializer, OrderSerializer
from user.serializers import UserSerializer, AuthTokenSerializer
from django.core.mail import send_mail, EmailMessage
import random, time, datetime
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from django.utils import timezone

# Create your views here.
class Cart(APIView):

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
            
            # Get profile
            user_id = Token.objects.get(key=request.auth.key).user_id
            customer = Customer.objects.get(user=user_id)
            address = Customer.objects.get(user=user_id).address

            # Check whether customer has any order that is not delivered
            if Order.objects.filter(customer = customer):
                return Response({"status": "failed", "error": "Your last order must be completed."})

            # Check Address
            # try:
            #     request.data.get("address",)
            # except:
            #     return Response({"status": "Address is required."})

            # Get Order Details
            order_details = request.data.get("order_details",)

            order_total = 0
            for dish in order_details:
                order_total += Dish.objects.get(id = dish["dish_id"]).price * dish["quantity"]

            if len(order_details) > 0:
                # Step 1 - Create an Order
                order = Order.objects.create(
                    customer = customer,
                    restaurant_id = request.data.get('restaurant_id',),
                    total = order_total,
                    # status = Order.COOKING,
                    address = address
                )

                # Step 2 - Create Order details
                for dish in order_details:
                    OrderDetails.objects.create(
                        order = order,
                        dish_id = dish["dish_id"],
                        quantity = dish["quantity"],
                        sub_total = Dish.objects.get(id = dish["dish_id"]).price * dish["quantity"]
                    )

                return Response({"status": "success"})

class CreateDeliveryDetails(APIView):
    serializer_class = CustomerSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        data = request.data
        user_id = Token.objects.get(key=request.auth.key).user_id

        try:
            phone = data.get('phone',)
        except:
            return Response({'status': 'Kindly enter your phone number'})
        
        try:
            address = data.get('address',)
        except:
            return Response({'status': 'Kindly enter your delivery address'})

        data['user'] = user_id
        serializer = self.serializer_class(data=data,context={'request': request} )

        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Customer Delivery Details addedz successfully'})
        return Response({'status': 'Failed to Create Customer Details.'})

class LatestOrder(APIView):
    serializer_class = OrderSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        
        user_id = Token.objects.get(key=request.auth.key).user_id
        customer = Customer.objects.get(user=user_id)
        order = OrderSerializer(Order.objects.filter(customer = customer).last()).data

        return Response({"order": order})

        
        
        
        


