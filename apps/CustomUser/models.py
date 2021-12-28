from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.conf import settings
from enum import Enum

class Gender(Enum):
    male=1
    female=2
    nonBinary=3

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='user', on_delete=models.CASCADE, null=True)
    firstname = models.CharField(max_length=24, null=True)
    lastname = models.CharField(max_length=24, null=True)
    phone = models.TextField(null=True,blank=True)
    avatar = models.ImageField(upload_to='avatar/',null=True, blank=True)
    coverImage = models.ImageField(upload_to='coverImage/',null=True, blank=True)
    bio=models.TextField(null=True,blank=True)
    gender=models.IntegerField(choices=((gender.value, gender.name) for gender in Gender),default=1)
    isPhoneVerified = models.BooleanField(default=False)

    def __str__(self):
        return (self.firstname + self.lastname) if self.firstname is not None and self.lastname is not None else self.user.username

class User(AbstractUser):
    email = models.EmailField(('email address'), unique=True)
    is_active=models.BooleanField(default=True)
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def __str__(self):
        return self.username



