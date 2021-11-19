from typing import List
from django.db.models import deletion
from rest_framework import generics, serializers, status, authentication, permissions
from core.models import *
from order.models import *
from order.serializers import CustomerSerializer, OrderDetailsSerializer, OrderSerializer
from django.core.mail import send_mail, EmailMessage
import random, time, datetime
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from django.utils import timezone
from rest_framework import status

# Create your views here.
class CartView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        user_id = request.user.id
        user = request.user
        request_address_id = request.data.get('delivery_id', )
        request_address = request.data.get('address', )

        try:
            customer = Customer.objects.filter(user=user_id)
            if len(customer)>0 and request_address_id:
               customer = customer[request_address_id-1]
            else:
               customer = customer[0]
        except:
            return Response({"status": "Enter your delivery details"}, status=status.HTTP_400_BAD_REQUEST)
                 
        address = customer.address  

        order_details = request.data.get("order_details",)

        order_total = 0
        for dish in order_details:
            order_total += Dish.objects.get(id = dish["dish_id"]).price * dish["quantity"]

        if len(order_details) > 0:

            # if Order.objects.filter(user = user).exists():
            #     order = Order.objects.update(
            #         customer = customer,
            #         restaurant_id = request.data.get('restaurant_id',),
            #         total = order_total,
            #         address = address)
                
            #     for dish in order_details:
            #         OrderDetails.objects.update(
            #             order = order,
            #             dish_id = dish["dish_id"],
            #             quantity = dish["quantity"],
            #             sub_total = Dish.objects.get(id = dish["dish_id"]).price * dish["quantity"]
            #         )

            #     return Response({"status": "Items updated successfully"}, status=status.HTTP_202_ACCEPTED)

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

    def put(self, request):
            
        user_id = request.user.id
        user = request.user
        request_address_id = request.data.get('delivery_id', )
        request_address = request.data.get('address', )

        try:
            customer = Customer.objects.filter(user=user_id)
            if len(customer)>0 and request_address_id:
               customer = customer[request_address_id-1]
            else:
               customer = customer[0]
        except:
            return Response({"status": "Enter your delivery details"}, status=status.HTTP_400_BAD_REQUEST)

        
        if request_address:
            address = request_address
        
        elif request_address_id:
            address = Customer.objects.filter(user=user_id)[request_address_id-1].address
            
        else:    
            address = Customer.objects.filter(user=user_id)[0].address


        order_details = request.data.get("order_details",)

        order_total = 0
        for dish in order_details:
            order_total += Dish.objects.get(id = dish["dish_id"]).price * dish["quantity"]

        if len(order_details) > 0:

            if Order.objects.filter(user = user).exists(): 
        
                order1 = Order.objects.get(
                    customer = customer,
                    restaurant_id = request.data.get('restaurant_id',))
                
                order1.customer = customer
                order1.total = order_total
                order1.address = address
                order1.save()

                
                for dish in order_details:
                    order_details1 = OrderDetails.objects.get(
                        order = order1,
                        dish_id = dish["dish_id"],
                    )
                    order_details1.order = order1
                    order_details1.dish_id = dish['dish_id']
                    order_details1.quantity = dish['quantity']
                    order_details1.sub_total = Dish.objects.get(id = dish['dish_id']).price * dish['quantity']
                    order_details1.save()
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

    

# class DeleteCartView(APIView):

#     def delete(self, request):

#         order_id = request.data.get("order_id")
#         user = request.user
#         # order = Order.objects.get(id = order_id)
#         # return Response({'status': "You don't have anything in cart."})
#         try:
#             cart = Cart.objects.latest('id')
#         except:
#             return Response({"status": "Current cart deleted."})
#         cart.delete()

#         return Response({'status': 'Product removed from Cart'}, status=status.HTTP_204_NO_CONTENT)

         
class DeliveryDetails(APIView):
    serializer_class = CustomerSerializer

    def get(self, request):
        
        user = request.user
        print(Customer.objects.filter(user=user))
        serializer = self.serializer_class(Customer.objects.filter(user=user), many=True).data
        return Response(serializer, status=status.HTTP_200_OK)


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

class DeleteDeliveryDetails(APIView):

    def delete(self, request, delivery_id):
        
        user = request.user
        try:
            delivery = Customer.objects.filter(user = user)
        except:
            return Response({"status": "No Delivery Details"}, status=status.HTTP_400_BAD_REQUEST)
    
        address = Customer.objects.filter(user = user)[delivery_id-1].address
        print(address)
        delete_delivery = Customer.objects.get(user = user, address=address)
        delete_delivery.delete()
        return Response({'status': 'Delivery details removed.'}, status=status.HTTP_204_NO_CONTENT)

class LatestOrder(APIView):
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        
        user = request.user
        # customer = Customer.objects.filter(user=user)
        order = OrderSerializer(Order.objects.filter(user = user).last()).data

        return Response({"order": order})

class GetAllCustomerOrder(APIView):
    serializer_class = OrderSerializer
    def get(self, request, *args, **kwargs):
        
        user = request.user
        # customer = Customer.objects.filter(user=user)
        order = OrderSerializer(Order.objects.filter(user = user), many=True).data

        return Response({"order": order})

class OrderView(APIView):

    def get(self, request, format=None):

        user = User.objects.get(id = request.user.id)

        if Order.objects.filter(user = user).exists():
            order = Order.objects.get(user = user)
        else:
            order = Order.objects.create(user = user)

        dish = OrderDetails.objects.filter(order = order)
        serializer = OrderDetailsSerializer(dish, many = True)
        return Response(serializer.data)

    def put(self, request, format = None):
            
            user = request.user

            dish = Dish.objects.get(id = request.data.get('dish_id',))
            cart = Cart.objects.get_or_create(user = user, dish = dish)

            if cart.exists():
                order = cart[0]
                # order.items.add(order_item)
                return Response(data={'details':"item added to cart"},status=status.HTTP_201_CREATED)
            else:
                ordered_date = timezone.now()
                order       = Cart.objects.create(user=request.user, ordered_date=ordered_date)
                # order.items.add(order_item)
                return Response(data={"details":"item added to your cart"})
            