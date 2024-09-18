from django.db import models
from django.contrib.auth.models import AbstractUser

class PrivateUser(AbstractUser):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    username = models.CharField(max_length=33, unique=True) # To preserve superuser
    # ^ This field will store a secret token for Google Auth QR
    email = models.EmailField(max_length=256, unique=True)
    age = models.IntegerField()
    has_2fa = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'age', 'username']

class PublicUser(models.Model):
    user = models.OneToOneField(PrivateUser, on_delete=models.CASCADE)
    location = models.CharField(max_length=52)
    gender = models.CharField(max_length=25)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    bio = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class UserInterests(models.Model):
    interest = models.CharField(max_length=32)
    user = models.ForeignKey(PublicUser, on_delete=models.CASCADE)


