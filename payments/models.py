from django.db import models
from seller.models import Dish


class Price(models.Model):
    # dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    stripe_price_id = models.CharField(max_length=100)
    price = models.IntegerField(default=0)  # cents
	
    def get_display_price(self):
        return "{0:.2f}".format(self.price/100)
