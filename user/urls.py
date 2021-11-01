from django.urls import path

from user import views
from rest_framework.authtoken.views import obtain_auth_token


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('password/reset/', views.PasswordReset.as_view(), name='passwordreset'),
    path('password/reset/verify/', views.PasswordResetOTPConfirm.as_view(), name='passwordresetconfirmation'),
    path('login/', obtain_auth_token, name = 'login'),
    path('loginnn/', views.loginOTP.as_view(), name = 'loginotp'),
    path('login/verify', views.loginOTPverification.as_view(), name = 'loginotpverification'),

]
