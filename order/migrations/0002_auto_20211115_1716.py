# Generated by Django 3.2.8 on 2021-11-15 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='order_payment_id',
            field=models.CharField(default=0, max_length=100),
        ),
    ]
