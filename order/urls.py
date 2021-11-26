from django.urls import path
from order.views import CheckoutView, DeleteCartView, DeliveryDetails,LatestOrder, DeleteDeliveryDetails, GetAllCustomerOrder, OrderView    


urlpatterns = [
    path('addordercart/', OrderView.as_view(), name = 'cartaddorder'),
    path('delivery/', DeliveryDetails.as_view(), name='deliverydetails'),
    path('deletedelivery/<int:delivery_id>', DeleteDeliveryDetails.as_view(), name='deletedeliverydetails'),
    # path('deletecart/', DeleteCartView.as_view(), name='deletedeliverydetails'),
    path('order/latest', LatestOrder.as_view(), name = 'latest-order' ),
    path('order/all', GetAllCustomerOrder.as_view(), name = 'all-customer-order'),
    path('checkout/', CheckoutView.as_view(), name = 'checkout'),
    path('deletecart/', DeleteCartView.as_view(), name='delete cart')
]
