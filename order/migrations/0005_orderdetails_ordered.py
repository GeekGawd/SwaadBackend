# Generated by Django 3.2.9 on 2021-11-25 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_cartmodel_order_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
    ]