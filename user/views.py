from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from core.models import *
from user.serializers import UserSerializer, AuthTokenSerializer
from django.core.mail import send_mail, EmailMessage
import random, time, datetime
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from django.utils import timezone


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer
    

class LoginView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

def login_send_otp_email(email,subject):
    
    OTP.objects.filter(otp_email__iexact = email).delete()

    otp = random.randint(1000,9999)

    msg = EmailMessage(subject, '<div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2"><div style="margin:50px auto;width:70%;padding:20px 0"><div style="border-bottom:1px solid #eee"><a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">Swaad</a></div><p style="font-size:1.1em">Hi,</p><p>Thank you for creating an account on Swaad. Use the following OTP to complete your Sign Up procedures. OTP is valid for 2 minutes</p><h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{otp}</h2><p style="font-size:0.9em;">Regards,<br/>Suyash Singh<br>CEO</p><hr style="border:none;border-top:1px solid #eee" /><div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300"><p>Swaad</p><p>Chinchpokli Bunder, Khau Galli</p><p>Jaunpur</p></div></div></div>' , 'suyashsingh.stem@gmail.com', (email,))
    msg.content_subtype = "html"
    msg.send()

    OTP.objects.create(otp=otp, otp_email = email)

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


class LoginOTP(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        
        request_email = request.data.get("email",)
       
        if request_email:
            try:
                user = User.objects.get(email__iexact = request_email)
            except:
                return Response({
                    'validation':False,
                    'status':'There is no such email registered'
                })
            login_send_otp_email(request_email,subject="[OTP] New Login for Swaad App") 
            return Response({"status":"The OTP has been sent to the mail id"},status = status.HTTP_200_OK)
            
            
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
                raise Http404
            
            otp = request_model.otp
            email = request_model.otp_email

            request_time = OTP.objects.get(otp_email__iexact = request_email).time_created + datetime.timedelta(seconds = 120)
            current_time = timezone.now()

            if request_time < current_time:
                return Response({"status" : "Sorry, entered OTP has expired.",
                                 "time": str(request_time)},status = status.HTTP_400_BAD_REQUEST)
            
            if str(request_otp) == str(otp) and request_email == email:
                user.object.is_verified = True
                request_model.save()
                return Response({
                    'verified':True,
                    'status':'OTP verified, proceed to registration.'
                })
            else:
                return Response({
                    'verified':False,
                    'status':'OTP incorrect.'

                })