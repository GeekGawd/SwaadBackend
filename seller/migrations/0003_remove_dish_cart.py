# Generated by Django 3.2.9 on 2021-11-20 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0002_dish_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='cart',
        ),
    ]