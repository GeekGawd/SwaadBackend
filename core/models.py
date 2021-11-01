from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.utils import timezone
from rest_framework.response import Response



class UserManager(BaseUserManager):

    def create_user(self, email, name, password=None, **extra_fields):
        if email is None:
            return Response({'status':'Users must have an email address'})
        if name is None:
            return Response({'status':'Users must have a name'})
        if password is None:
            return Response({'status':'Users must have a password'})
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class OTP(models.Model):
    otp          = models.IntegerField()
    otp_email    = models.EmailField()
    time_created = models.DateTimeField(default=timezone.now )
    def __str__(self):
        return f"{self.otp_email} : {self.otp}"
