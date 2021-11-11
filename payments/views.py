from django.shortcuts import render, redirect

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from .models import Price

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        price = Price.objects.get(id=self.kwargs["pk"])
        YOUR_DOMAIN = "http://127.0.0.1:8000"  # change in production
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return redirect(checkout_session.url)


from django.views.generic import TemplateView

class SuccessView(TemplateView):
    template_name = "success.html"

class CancelView(TemplateView):
    template_name = "cancel.html"


from seller.models import Dish

class ProductLandingPageView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        dish = Dish.objects.get(title="kachori")
        prices = Price.objects.filter(dish=dish)
        context = super(ProductLandingPageView,
                        self).get_context_data(**kwargs)
        context.update({
            "dish": dish,
            "prices": prices
        })
        return context