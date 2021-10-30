from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from core.models import *
from user.serializers import UserSerializer, AuthTokenSerializer
from django.core.mail import send_mail
import random, time
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

def send_otp_email(email,body,subject):
    # OTP.objects.filter(otp_email__iexact = email).delete()
    otp = random.randint(999,9999)
    time_of_creation = int(time.time())

    send_mail(
    subject,
    f"{body} {otp}.\n This OTP will be valid for 1 minute." 
    ,'info.the.flow.app@gmail.com',
    [email],
     fail_silently = False
     ) 

    OTP.objects.create(otp=otp, otp_email = email, time_created = time_of_creation)

class PasswordResetView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        request_email = request.data.get("email", )

        otp = OTP.objects.filter(otp_email = request_email).first()

        try:
            user = User.objects.get(email__iexact = request_email)
        except: 
            return Response({"detail" : "No such account exists"},status = status.HTTP_400_BAD_REQUEST)


        if (int(time.time() - otp.time_created )):
            return Response({"detail":"OTP was sent less than a minute ago."},status=status.HTTP_400_BAD_REQUEST)

        # if not user.is_active:
        #     send_otp_email(request_email, body = f"You have not verified your email {request_email} yet. This email will let you change your  password and Verify your email in a single step. Your OTP for the same is",
        #     subject= "Verify email and change password OTP for The Flow App")
        #     return Response({"detail" : "User is registered but not verified. An OTP for verification has been sent to email."}, status = status.HTTP_200_OK)


        send_otp_email(request_email, body = "OTP for resetting your password of your The Flow App account is",subject="Password Change OTP for The Flow App") 

        return Response({"detail" : "OTP has been sent to your provided email."}, status = status.HTTP_200_OK)