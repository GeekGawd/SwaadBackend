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
from django.http import Http404
from django.utils import timezone


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        request_email = request.data.get('email',)
        try:
             user = User.objects.get(email__iexact = request_email)
        except:
            if serializer.is_valid():
                serializer.save()
                return Response({'status' : 'User registered successfully'})
            return Response({'status' : 'Registration was not successful. Please enter the details carefully.'})
        return Response({'status' : 'Entered email is already registered.'})
        

class LoginView(ObtainAuthToken):
    """Create a new auth token for user"""
    # serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    def post(self, request, *args, **kwargs):
        request_email = request.data.get('email',)
        try:
            user1 = User.objects.get(email__iexact = request_email)
        except: 
            return Response({
                'status':'User not registered'
            })
        if user1.is_active is True:
            serializer = AuthTokenSerializer(data=request.data,  context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            name = user1.name
            return Response({
                'token': token.key,
                'name': name
                })
        else:
            return Response({
                'status':'User not validated, please goto login/otp'
            })


def login_send_otp_email(email,subject):
    
    OTP.objects.filter(otp_email__iexact = email).delete()

    otp = random.randint(1000,9999)

    msg = EmailMessage(subject, f'<div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2"><div style="margin:50px auto;width:70%;padding:20px 0"><div style="border-bottom:1px solid #eee"><a href="" style="font-size:2em;color: #FFD243;text-decoration:none;font-weight:600">Swaad</a></div><p style="font-size:1.2em">Greetings,</p><p style="font-size:1.2em"> Thank you for creating an account on Swaad. You can count on us for quality, service, and selection. Now, we would not like to hold you up, so use the following OTP to complete your Sign Up procedures and order away.<br><b style="text-align: center;display: block;">Note: OTP is only valid for 5 minutes.</b></p><h2 style="font-size: 1.9em;background: #FFD243;margin: 0 auto;width: max-content;padding: 0 15px;color: #fff;border-radius: 4px;">{otp}</h2><p style="font-size:1.2em;">Regards,<br/>Team Swaad</p><hr style="border:none;border-top:1px solid #eee" /><div style="float:right;padding:8px 0;color:#aaa;font-size:1.2em;line-height:1;font-weight:500"><p>Swaad</p><p>Boys Hostel, Near Girl Hostel AKGEC</p><p>Ghaziabad</p></div></div></div>', 'swaad.info.contact@gmail.com', (email,))
    msg.content_subtype = "html"
    msg.send()

    time_created = int(time.time())

    OTP.objects.create(otp=otp, otp_email = email, time_created = time_created)

def send_otp_email(email,subject):
    
    OTP.objects.filter(otp_email__iexact = email).delete()

    otp = random.randint(1000,9999)

    msg = EmailMessage(subject, f'<div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2"><div style="margin:50px auto;width:70%;padding:20px 0"><div style="border-bottom:1px solid #eee"><a href="" style="font-size:2em;color: #FFD243;text-decoration:none;font-weight:600">Swaad</a></div><p style="font-size:1.2em">Greetings,</p><p style="font-size:1.2em"> Looks like you forgot your password. No worries we are here to help you recover your account. Use the following OTP to recover your account and start ordering the delicacies again in no time. <br><b style="text-align: center;display: block;">Note: OTP is only valid for 5 minutes.</b></p><h2 style="font-size: 1.9em;background: #FFD243;margin: 0 auto;width: max-content;padding: 0 15px;color: #fff;border-radius: 4px;">{otp}</h2><p style="font-size:1.2em;">Regards,<br/>Team Swaad</p><hr style="border:none;border-top:1px solid #eee" /><div style="float:right;padding:8px 0;color:#aaa;font-size:1.2em;line-height:1;font-weight:500"><p>Swaad</p><p>Boys Hostel, Near Girl Hostel AKGEC</p><p>Ghaziabad</p></div></div></div>' , 'swaad.info.contact@gmail.com', (email,))
    msg.content_subtype = "html"
    msg.send()

    time_created = int(time.time())

    OTP.objects.create(otp=otp, otp_email = email, time_created = time_created)

class PasswordReset(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        request_email = request.data.get("email", )

        try:
            user = User.objects.get(email__iexact = request_email)
        except: 
            return Response({"status" : "No such account exists"},status = status.HTTP_400_BAD_REQUEST)

        if hasattr(user, 'auth_token'):
            user.auth_token.delete()

        send_otp_email(email = request_email,subject="[OTP] Password Change for Swaad App") 

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

            request_time = otpfields.time_created
            current_time = int(time.time())

            if current_time - request_time > 300:
                return Response({"status" : "Sorry, entered OTP has expired."},status = status.HTTP_400_BAD_REQUEST)

            if str(otpfields.otp) != str(request_otp):
                 return Response({"status" : "Sorry, entered OTP doesn't match the sent OTP."},status = status.HTTP_400_BAD_REQUEST)

            OTP.objects.filter(otp_email__iexact = request_email).delete()
            token, created = Token.objects.get_or_create(user=user)
            return Response({"status": "OTP verified You can now change your password", "token": token.key}, status = status.HTTP_200_OK)

        return Response({"status": "Please Provide an email address"},status = status.HTTP_400_BAD_REQUEST)


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
                login_send_otp_email(request_email,subject="[OTP] New Login for Swaad App") 
                return Response({"status":"The OTP has been sent to the mail id"},status = status.HTTP_200_OK)
            else:
                return Response({"status":"please enter an email id"},status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status":"user registered already"},status = status.HTTP_400_BAD_REQUEST)
                
            
            
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

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user