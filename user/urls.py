from django.urls import path
from user import views



app_name = 'user'

urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('password/reset/', views.PasswordReset.as_view(), name='passwordreset'),
    path('password/reset/verify/', views.PasswordResetOTPConfirm.as_view(), name='passwordresetconfirmation'),
    path('login/otp', views.LoginOTP.as_view(), name = 'loginotp'),
    path('login/verify', views.LoginOTPverification.as_view(), name = 'loginotpverification'),
]
