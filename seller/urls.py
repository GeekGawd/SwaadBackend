from django.urls import path, include
from .views import RestaurantViewSet
from rest_framework.routers import DefaultRouter
from seller import views


# category_list = CategoryViewSet.as_view({
#     'get': 'list',
#     'post': 'create',
# })

# category_detail = CategoryViewSet.as_view({
#     'get':'retrieve',
#     'put': 'update',
#     'delete': 'destroy',
# })
# restaurant_list = RestaurantViewSet.as_view({
#     'get': 'list',
#     'post': 'create',
# })

# restaurant_detail = RestaurantViewSet.as_view({
#     'get':'retrieve',
#     'put': 'update',
#     'delete': 'destroy',
# 



# router = DefaultRouter(trailing_slash=False)
# router.register('restaurants', RestaurantViewSet)
urlpatterns = [
    # path('', include(router.urls)),
    path('register/', views.CreateSellerView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('customer/restaurants/', views.CustomerGetRestaurants.as_view()),
    path('customer/rating/<dish_id>', views.CustomerRating.as_view()),
    path('customer/rating', views.CustomerRating.as_view()),
    path('customer/dish/<restaurant_id>/', views.CustomerGetDish.as_view()),
    path('restaurant/addmeal', views.RestaurantAddDish.as_view()),
    path('login/otp', views.LoginOTP.as_view(), name = 'loginotp'),
    path('login/verify', views.LoginOTPverification.as_view(), name = 'loginotpverification'),
]