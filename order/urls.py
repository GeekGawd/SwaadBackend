from django.urls import path
from order.views import Cart, CreateDeliveryDetails, LatestOrder, GetAllCustomerOrder


urlpatterns = [
    path('addorder', Cart.as_view(), name = 'cartaddorder'),
    path('delivery/create', CreateDeliveryDetails.as_view(), name='createdeliverydetails'),
    path('order/latest', LatestOrder.as_view(), name = 'latest-order' ),
    path('order/latest', GetAllCustomerOrder.as_view(), name = 'all-customer-order')
]
