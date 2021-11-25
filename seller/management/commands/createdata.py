from random import randint, choice
from django.core.mail import mail_managers
from django.core.management.base import BaseCommand
from faker import Faker
from core.models import User
from seller.models import Dish, Restaurant
import faker.providers

CATEGORIES = [
    "Sweets",
    "Rolls",
    "Kebabs",
    "Chaat",
    "Paneer",
    "Pizza",
    "Chicken",
    "Healthy",
    "Biryani",
    "Shawarma",
    "Thali",
    "Momos",
    "Burger",
    "Dal",
    'Dosa',
    "Chaap",
]

MEAL_TIME = [
    "Breakfast",
    "Lunch",
    "Dinner"
]

class Provider(faker.providers.BaseProvider):
    def dish_category(self):
        return self.random_element(CATEGORIES)
    
    def dish_meal_time(self):
        return self.random_element(MEAL_TIME)

class Command(BaseCommand):
    help = 'Command Information'

    def handle(self, *args, **kwargs):
        fake = Faker(["en_IN"])
        fake.add_provider(Provider)
        
        for _ in range(15):
            mail = fake.email()
            name = fake.name()
            is_active = True

            user = User.objects.create(
                email = mail,
                name = name,
                is_active = is_active
            )

            user.set_password("Test@1234")
            user.save()

        for _ in range(1, 16):
            user_id = _
            user = User.objects.get(id = user_id)
            rest_name = fake.company()
            phone = fake.phone_number()
            address = fake.address()
            address = address.replace("\n", ",")
            pic = choice([i for i in range(1,8)])
            product_img = f'restaurant/p{pic}'
            delivery_time = randint(31,61)
            Restaurant.objects.create(
                user = user,
                rest_name = rest_name,
                phone = phone,
                address = address,
                image = product_img,
                delivery_time = delivery_time
            )
        
        for _ in range(1, 150):
            rest_id = randint(1, 15)
            rest = Restaurant.objects.get(id = rest_id)
            temp = randint(50, 600)
            temp /= 10
            temp = round(temp)
            price = temp * 10
            title = fake.dish_category()
            category = fake.dish_category()
            dish_time = fake.dish_meal_time()
            pic = choice([i for i in range(1,20)])
            product_img = f'p{pic}'

            Dish.objects.create(
                restaurant = rest,
                price = price,
                title = title,
                category = category,
                Dish_time = dish_time,
                image = product_img
            )