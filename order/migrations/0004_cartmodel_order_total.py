# Generated by Django 3.2.9 on 2021-11-24 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20211121_0126'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartmodel',
            name='order_total',
            field=models.IntegerField(default=0),
        ),
    ]
