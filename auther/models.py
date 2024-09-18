from django.db import models
from django.contrib.auth.models import AbstractUser

class PrivateUser(AbstractUser):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    username = models.CharField(max_length=33, unique=True) # To preserve superuser
    # ^ This field will store a secret token for Google Auth QR
    email = models.EmailField(max_length=256, unique=True)
    age = models.IntegerField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'age', 'username']

class PublicUser(models.Model):
    user = models.OneToOneField(PrivateUser, on_delete=models.CASCADE)
    location = models.CharField(max_length=52)
    gender = models.CharField(max_length=25)
    bio = models.CharField(max_length=256)


class UserInterests(models.Model):
    interest = models.CharField(max_length=32)
    user = models.ForeignKey(PublicUser, on_delete=models.CASCADE)


