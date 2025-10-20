from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from user_profile_api.models import UserProfile
# Create your models here.

class CustomAuthManager(BaseUserManager):
    """
    Custom UserManager for creating a UserProfile after
    creating a User.
    """
    def _after_create_user(self, user):
        if user is None:
            raise ValueError('No user found')
        
        user_profile = UserProfile.objects.get_or_create(user=user)
        return user_profile

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be given!')
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        self._after_create_user(user)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be staff member!')
        
        if extra_fields.get('is_superuser')is not True:
            raise ValueError('Superuser needs superuser status!')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomAuthManager()

    def __str__(self):
	    return f"{self.email}"
