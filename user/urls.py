from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),

    path('login/', views.LoginView.as_view(), name='login'),

    path('password/reset/', views.PasswordReset.as_view(), name='passwordreset'),

    path('password/reset/verify/', views.PasswordResetOTPConfirm.as_view(), name='passwordresetconfirmation'),

    path('signup/verify/', views.SignUpOTPVerification.as_view(), name = 'signupverification'),

    # path('signup/resend/<str:email>', views.login_send_otp_email, name = 'loginotpverification'),

    path('signup/sendotp/', views.SignUpOTP.as_view(), name = 'sendotp'),
     
    path('profile/', views.ManageUserView.as_view(), name='loggedinuser'),
]
