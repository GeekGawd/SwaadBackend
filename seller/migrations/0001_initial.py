<<<<<<< HEAD
# Generated by Django 3.2.8 on 2021-11-12 08:12
=======
# Generated by Django 3.2.9 on 2021-11-11 14:50
>>>>>>> f917b26c3852b4ca8eae54401600f2780927b07e

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rest_name', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=500)),
                ('address', models.CharField(max_length=500)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
<<<<<<< HEAD
                ('photo', models.ImageField(upload_to='img/Dish_images')),
=======
                ('photo', models.ImageField(blank=True, null=True, upload_to='img/Dish_images')),
>>>>>>> f917b26c3852b4ca8eae54401600f2780927b07e
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('title', models.CharField(max_length=200)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('veg', models.BooleanField(default=True)),
                ('category', models.CharField(choices=[('Sweets', 'Sweets'), ('Rolls', 'Rolls'), ('Kebab', 'Kebab'), ('Chaat', 'Chaat'), ('Paneer', 'Paneer'), ('Pizza', 'Pizza'), ('Chicken', 'Chicken'), ('Healthy', 'Healthy'), ('Biryani', 'Biryani'), ('Shawarma', 'Shawarma'), ('Thali', 'Thali'), ('Momos', 'Momos'), ('Burger', 'Burger'), ('Dal', 'Dal'), ('Dosa', 'Dosa'), ('Chaap', 'Chaap')], max_length=15)),
                ('Dish_time', models.CharField(blank=True, choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner')], default=FileNotFoundError, max_length=15, null=True)),
<<<<<<< HEAD
                ('favourite', models.BooleanField(default=False)),
=======
>>>>>>> f917b26c3852b4ca8eae54401600f2780927b07e
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.dish')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.restaurant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'dish')},
                'index_together': {('user', 'dish')},
            },
        ),
    ]
