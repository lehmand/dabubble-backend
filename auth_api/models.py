from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as CustomManager
# Create your models here.

class UserManager(CustomManager):
    """
    Custom UserManager for creating a UserProfile after
    creating a User.
    """
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_stuff', False)
        extra_fields.setdefault('is_superuser', False)
        return super().create_user(username, email, password, **extra_fields)
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_stuff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_stuff') is not True:
            raise ValueError('Superuser must be stuff member!')
        
        if extra_fields.get('is_superuser')is not True:
            raise ValueError('Superuser needs superuser status!')

        return super().create_superuser(username, email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomManager()

    def __str__(self):
	    return f"{self.email}"
