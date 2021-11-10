# Generated by Django 3.2.8 on 2021-11-08 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0004_auto_20211108_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='meal_time',
            field=models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner')], default=FileNotFoundError, max_length=15),
        ),
    ]