from typing import List
from rest_framework import generics, serializers, status, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from rest_framework.utils.serializer_helpers import ReturnDict
from core.models import *
from order.models import *
from order.serializers import CustomerSerializer, OrderSerializer
from django.core.mail import send_mail, EmailMessage
import random, time, datetime
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from django.utils import timezone
from rest_framework import status

# Create your views here.
class OrderView(APIView):

    permission_classes = [AllowAny]
    def put(self, request):
            
        user_id = request.user.id

        try:
            customer = Customer.objects.get(user=user_id)
        except:
            return Response({"status": "Enter your delivery details"}, status=status.HTTP_400_BAD_REQUEST)
        
        request_address = request.data.get('address', )
        request_address_id = request.data.get('delivery_id', )

        if request_address:
            address = request_address
        
        elif request_address_id:
            address = Customer.objects.get(user=user_id).address
            
        else:    
            address = Customer.objects.get(user=user_id).address
        
        

        user = request.user
        # if Order.objects.filter(customer = customer):
        #     return Response({"status":"Your last order must be completed."})

        # try:
        #     request.data.get("address",)
        # except:
        #     return Response({"status": "Address is required."})

        order_details = request.data.get("order_details",)

        order_total = 0
        for dish in order_details:
            order_total += Dish.objects.get(id = dish["dish_id"]).price * dish["quantity"]

        if len(order_details) > 0:

            if Order.objects.filter(user = user).exists():
                order = Order.objects.update(
                    customer = customer,
                    restaurant_id = request.data.get('restaurant_id',),
                    total = order_total,
                    address = address)
                
                for dish in order_details:
                    OrderDetails.objects.update(
                        order = order,
                        dish_id = dish["dish_id"],
                        quantity = dish["quantity"],
                        sub_total = Dish.objects.get(id = dish["dish_id"]).price * dish["quantity"]
                    )

                return Response({"status": "Items updated successfully"}, status=status.HTTP_202_ACCEPTED)

            else:
                order = Order.objects.create(user = user,
                    customer = customer,
                    restaurant_id = request.data.get('restaurant_id',),
                    total = order_total,
                    address = address)

                for dish in order_details:
                    OrderDetails.objects.create(
                        order = order,
                        dish_id = dish["dish_id"],
                        quantity = dish["quantity"],
                        sub_total = Dish.objects.get(id = dish["dish_id"]).price * dish["quantity"]
                    )

                return Response({"status": "Items added successfully"}, status=status.HTTP_201_CREATED)

    # def put(self, request, *args, **kwargs):
        
    #     order_details = request.data.get("order_details",)

    #     order_total = 0
    #     for dish in order_details:
    #         order_total += Dish.objects.get(id = dish["dish_id"]).price * dish["quantity"]

         
        


class CreateDeliveryDetails(APIView):
    serializer_class = CustomerSerializer

    def post(self, request, *args, **kwargs):

        data = request.data
        user_id = request.user.id

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
            return Response({'status': 'Customer Delivery Details added successfully'})
        return Response({'status': 'Failed to Create Customer Details.'})

class LatestOrder(APIView):
    serializer_class = OrderSerializer
    
    def get(self, request, *args, **kwargs):
        
        user_id = request.user.id
        customer = Customer.objects.get(user=user_id)
        order = OrderSerializer(Order.objects.filter(customer = customer).last()).data

        return Response({"order": order})

class GetAllCustomerOrder(APIView):
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        
        user_id = request.user.id
        customer = Customer.objects.get(user=user_id)
        order = OrderSerializer(Order.objects.filter(customer = customer)).data

        return Response({"order": order})

class Cart(APIView):

    def put(self, request, *args, **kwargs):
        
        user_id = request.user.id
        dish = Dish.objects.get(request.data.get("dish_id"),)
        # quan

        try:
            Customer.objects.get(user=user_id)
        except:
            return Response({"status": "Add your address and phone."}, status=status.HTTP_400_BAD_REQUEST)