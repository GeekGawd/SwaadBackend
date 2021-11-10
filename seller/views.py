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

def login_send_otp_email(email,subject):
    
    OTP.objects.filter(otp_email__iexact = email).delete()

    otp = random.randint(1000,9999)

    msg = EmailMessage(subject, f'<div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2"><div style="margin:50px auto;width:70%;padding:20px 0"><div style="border-bottom:1px solid #eee"><a href="" style="font-size:2em;color: #FFD243;text-decoration:none;font-weight:600">Swaad</a></div><p style="font-size:1.2em">Greetings,</p><p style="font-size:1.2em"> Thank you for creating an account on Swaad. You can count on us for quality, service, and selection. Now, we would not like to hold you up, so use the following OTP to complete your Sign Up procedures.<br><b style="text-align: center;display: block;">Note: OTP is only valid for 5 minutes.</b></p><h2 style="font-size: 1.9em;background: #FFD243;margin: 0 auto;width: max-content;padding: 0 15px;color: #fff;border-radius: 4px;">{otp}</h2><p style="font-size:1.2em;">Regards,<br/>Team Swaad</p><hr style="border:none;border-top:1px solid #eee" /><div style="float:right;padding:8px 0;color:#aaa;font-size:1.2em;line-height:1;font-weight:500"><p>Swaad</p><p>Boys Hostel, Near Girl Hostel AKGEC</p><p>Ghaziabad</p></div></div></div>', 'swaad.info.contact@gmail.com', (email,))
    msg.content_subtype = "html"
    msg.send()

    time_created = int(time.time())

    OTP.objects.create(otp=otp, otp_email = email, time_created = time_created)


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
        return Response({'details':'User already have a restaurant.'},status=status.HTTP_400_BAD_REQUEST)

class LoginView(ObtainAuthToken):
    """Create a new auth token for user"""
    # serializer_class = AuthTokenSerializer
    # renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    def post(self, request, *args, **kwargs):
        request_email = request.data.get('email',)
        try:
            user1 = User.objects.get(email__iexact = request_email)
            user1.restaurant
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
                'status':'User is not validated. Please verify the registered email id'
            })

class CustomerGetRestaurants(APIView):
    
    def get(self, request, *args, **kwargs):
        restaurants = RestaurantSerializer(
            Restaurant.objects.all().order_by("?"),
            many = True,
            context = {"request": request}
        ).data

        return Response({"restaurants": restaurants})


class RestaurantAddDish(APIView):

    serializer_class = DishSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # data = request.data
        # serializer = self.serializer_class(data = data)

        # if serializer.is_valid:
        #     serializer.save()
        #     return Response({"status": "Meal Added"})
        # return Response({"status": "Meal not added"})

        id1=request.user.id
        try:
            user    = User.objects.get(id=id1)
        except:
            raise Response({"status":"User Not Found"})
        serializer  = self.serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginOTP(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        request_email = request.data.get("email",)
        user = User.objects.get(email__iexact = request_email)
        if user.is_active is False:
            if request_email:
                try:
                    user = User.objects.get(email__iexact = request_email)
                except:
                    return Response({
                        'validation':False,
                        'status':'There is no such email registered'
                    })
                login_send_otp_email(request_email,subject="[OTP] Swaad Merchant Verification") 
                return Response({"status":"The OTP has been sent to the mail id"},status = status.HTTP_200_OK)
            else:
                return Response({"status":"Please enter an email id"},status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status":"User Verified Already"},status = status.HTTP_400_BAD_REQUEST)
                
class LoginOTPverification(APIView):
    permission_classes = [AllowAny]
    def post(self, request):

        request_otp   = request.data.get("otp",)
        request_email = request.data.get("email")

        if request_email:
            try:
                request_model = OTP.objects.get(otp_email__iexact = request_email)
                user = User.objects.get(email__iexact = request_email)
            except:
                return Response ({"status": "User is not Registered"})
            
            otp = request_model.otp
            email = request_model.otp_email

            request_time = OTP.objects.get(otp_email__iexact = request_email).time_created
            current_time = int(time.time())

            if current_time - request_time > 300:
                return Response({"status" : "Sorry, entered OTP has expired."}, status = status.HTTP_400_BAD_REQUEST)
            
            if str(request_otp) == str(otp) and request_email == email:
                request_model.save()
                OTP.objects.filter(otp_email__iexact = request_email).delete()
                user.is_active = True
                user.save()
                return Response({
                    'verified':True,
                    'status':'OTP verified, proceed to registration.'
                })
            else:
                return Response({
                    'verified':False,
                    'status':'OTP incorrect.'

                })

class CustomerGetDish(APIView):

    serializer_class = DishSerializer
    def get(self, request, restaurant_id):

        meals = self.serializer_class(
            Dish.objects.filter(restaurant_id = restaurant_id).order_by("id"),
            many = True,
            context = {"request": request}
        ).data

        return Response({"meals": meals})

class CustomerRating(APIView):

    serializer_class = RatingSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        ratings = RatingSerializer(
            Rating.objects.all().order_by('id'),
            many = True,
            context = {"request": request}
        ).data

        return Response({"ratings": ratings}, status=status.HTTP_200_OK)

    def post(self, request, dish_id=None):

        
        if 'stars' in request.data:
            stars = request.data['stars']
            user_id = Token.objects.get(key=request.auth.key).user_id
            # return Response({'status': user_id}, status=status.HTTP_200_OK)
            user = User.objects.get(id=user_id)
            dish = Dish.objects.get(id=dish_id)
            print("dish")
            restaurant = dish.restaurant
            try: 
                rating = Rating.objects.get(user=user, dish=dish.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {'status': 'Rating updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)

            except: 
                rating = Rating.objects.create(user=user, dish=dish, stars=stars, restaurant=restaurant)
                serializer = RatingSerializer(rating, many=False)
                response = {'status': 'Rating created', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
                 
        else:
            response = {'message': 'You need to provide a rating'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


