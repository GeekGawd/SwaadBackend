from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from core.models import *
from user.serializers import UserSerializer, AuthTokenSerializer
from django.core.mail import send_mail
import random, time, datetime
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from django.utils import timezone


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user when logging in"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

def send_otp_email(email,body,subject):
    
    OTP.objects.filter(otp_email__iexact = email).delete()

    otp = random.randint(1000,9999)

    send_mail(
    subject,
    f"{body} {otp}.\n This OTP will be valid for 2 minute." 
    ,'suyashsingh.stem@gmail.com',
    [email],
     fail_silently = False
     ) 

    OTP.objects.create(otp=otp, otp_email = email)

class PasswordReset(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        request_email = request.data.get("email", )

        try:
            user = User.objects.get(email__iexact = request_email)
        except: 
            return Response({"status" : "No such account exists"},status = status.HTTP_400_BAD_REQUEST)

        send_otp_email(request_email, body = "Hi! Sorry for the inconvenience. Here is your OTP for the Swaad App",subject="[OTP] Password Change for Swaad App") 

        return Response({"status" : "OTP has been sent to your email."}, status = status.HTTP_200_OK)


class PasswordResetOTPConfirm(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        data = request.data
        request_otp   = data.get("otp",)
        request_email = data.get("email",)

        if request_email:
            try:
                otpfields = OTP.objects.get(otp_email__iexact = request_email)
                user = User.objects.get(email__iexact = request_email)
            except:
                raise Http404

            request_time = otpfields.time_created + datetime.timedelta(seconds = 120)
            current_time = timezone.now()

            if request_time < current_time:
                return Response({"status" : "Sorry, entered OTP has expired.",
                                 "time": str(request_time)},status = status.HTTP_400_BAD_REQUEST)

            if str(otpfields.otp) != str(request_otp):
                 return Response({"status" : "Sorry, entered OTP doesn't match the sent OTP.",
                                 "time": str(request_time)},status = status.HTTP_400_BAD_REQUEST)

            OTP.objects.filter(otp_email__iexact = request_email).delete()
            return Response({"status": "OTP verified You can now change your password"}, status = status.HTTP_200_OK)


        return Response({"status": "Please Provide an email address"},status = status.HTTP_400_BAD_REQUEST)
