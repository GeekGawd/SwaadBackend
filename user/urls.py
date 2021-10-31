from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('password/reset/', views.PasswordReset.as_view(), name='passwordreset'),
    path('password/reset/verify/', views.PasswordResetOTPConfirm.as_view(), name='passwordresetconfirmation'),
]
