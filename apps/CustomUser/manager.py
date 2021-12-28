from django.contrib.auth.base_user import BaseUserManager
from . import models

class UserManager(BaseUserManager):
    def create_user(self, username,email, password, **extra_fields):
        if not email and username:
            raise ValueError(_('Email and Username must be set.'))
        email = self.normalize_email(email)
        
        user = self.model(email=email,username = username, **extra_fields)
        user.set_password(password)
        user.save()
        models.Profile.objects.create(user=user)
        return user

    def create_superuser(self, email,username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username,email, password, **extra_fields)
