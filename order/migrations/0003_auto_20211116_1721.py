# Generated by Django 3.2.8 on 2021-11-16 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20211115_1716'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='is_paid',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_payment_id',
        ),
    ]
