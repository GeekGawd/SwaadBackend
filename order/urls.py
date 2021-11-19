from django.urls import path
from order.views import CartAdd, CartView, DeliveryDetails, DeleteDeliveryDetails,LatestOrder, GetAllCustomerOrder, DeleteCartView


urlpatterns = [
    path('addordercart/', CartAdd.as_view(), name = 'cartaddorder'),
    path('delivery/', DeliveryDetails.as_view(), name='deliverydetails'),
    path('deletedelivery/<int:delivery_id>', DeleteDeliveryDetails.as_view(), name='deletedeliverydetails'),
    path('deletecart/', DeleteCartView.as_view(), name='deletedeliverydetails'),
    path('order/latest', LatestOrder.as_view(), name = 'latest-order' ),
    path('order/all', GetAllCustomerOrder.as_view(), name = 'all-customer-order'),
    path('checkout/', CartView.as_view(), name = 'checkout'),
]
