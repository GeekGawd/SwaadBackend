from django.urls import path
from order.views import Cart, CreateDeliveryDetails, LatestOrder


urlpatterns = [
    path('addorder', Cart.as_view(), name = 'cartaddorder'),
    path('delivery/create', CreateDeliveryDetails.as_view(), name='createdeliverydetails'),
    path('order/latest', LatestOrder.as_view(), name = 'latest order' )
]


