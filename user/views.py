from django.contrib.auth.models import Permission
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
from django.http import Http404


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

def send_otp_email(email,body,subject):
    OTP.objects.filter(otp_email__iexact = email).delete()
    otp = random.randint(1000,9999)
    time_of_creation = int(time.time())

    send_mail(
    subject,
    f"{body} {otp}.\n This OTP will be valid for 2 minute." 
    ,'suyashsingh.stem@gmail.com',
    [email],
     fail_silently = False
     ) 

    OTP.objects.create(otp=otp, otp_email = email, time_created = time_of_creation)

class PasswordReset(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        request_email = request.data.get("email", )

        try:
            user = User.objects.get(email__iexact = request_email)
        except: 
            return Response({"status" : "No such account exists"},status = status.HTTP_400_BAD_REQUEST)

        send_otp_email(request_email, body = "Hi! Thank You for the inconvenience. Here is your OTP for the Swaad App",subject="[OTP] Password Change for Swaad App") 

        return Response({"status" : "OTP has been sent to your email."}, status = status.HTTP_200_OK)


class PasswordResetOTPConfirm(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        coming_data = request.data
        request_otp   = coming_data.get("otp",)
        request_email = coming_data.get("email",)
        current_time = int(time.time())
        if request_email is not None:
            try:
                otpmodel = OTP.objects.get(otp_email__iexact = request_email)
                user = User.objects.get(email__iexact = request_email)
            except:
                raise Http404
            if otpmodel.otp_email == request_email and otpmodel.otp == request_otp and (current_time - otpmodel.time_created <120):
                OTP.objects.filter(otp_email__iexact = request_email).delete()
                return Response({"detail": "OTP verified Thank You!"}, status = status.HTTP_200_OK )
            return Response({"detail" : "OTP is wrong or alredy expired."},status = status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Provide an email to reset password."},status = status.HTTP_400_BAD_REQUEST)

class loginOTP(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        
        request_email = request.data.get("email")
       
        if request_email is not None:
            try:
                user = User.objects.get(email__iexact = request_email)
            except:
                return Response({
                    'validity':False,
                    'detail':'There is no such email registered'
                })
            send_otp_email(request_email, body = "Hi! Thank You for the inconvenience. Here is your OTP for your new login to the Swaad App",subject="[OTP] New Login for Swaad App") 
            return Response({"detail":"The OTP has been sent to the mail id"},status = status.HTTP_200_OK)
            
            
class loginOTPverification(APIView):
    permission_classes = [AllowAny]
    def post(self, request):

        request_otp   = request.data.get("otp",)
        request_email = request.data.get("email")

    
        if request_email is not None:
            try:

                request_model = OTP.objects.get(otp_email__iexact = request_email)
                user = User.objects.get(email__iexact = request_email)
            except:
                raise Http404
            if request_model.exists():
                # old = old.first()
                otp = request_model.otp
                email = request_model.otp_email
                if str(request_otp) == str(otp) and request_email == email:
                    request_model.validated = True
                    request_model.save()
                    return Response({
                        'validity':True,
                        'detail':'OTP verified, proceed to registration.'
                    })
                else:
                    return Response({
                        'validity':False,
                        'detail':'OTP incorrect.'

                    })
            else:
                return Response({
                        'validity':False,
                        'detail':'OTP not sent.'

                    })
        # else:
        #     return Response({
        #                 'validity':False,
        #                 'detail':'Please provide a valid email id.'

        #             })
