from django.urls import path
from order.views import Cart, CartView, DeliveryDetails, DeleteDeliveryDetails,LatestOrder, GetAllCustomerOrder


urlpatterns = [
    path('addordercart/', CartView.as_view(), name = 'cartaddorder'),
    path('delivery/', DeliveryDetails.as_view(), name='deliverydetails'),
    path('deletedelivery/<int:delivery_id>', DeleteDeliveryDetails.as_view(), name='deletedeliverydetails'),
    path('order/latest', LatestOrder.as_view(), name = 'latest-order' ),
    path('order/all', GetAllCustomerOrder.as_view(), name = 'all-customer-order')
]
