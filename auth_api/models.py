from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
	avatar_url = models.URLField(blank=True, null=True)
	is_online = models.BooleanField(default=False)
	last_login = models.DateTimeField(auto_now=True)
	is_activated = models.BooleanField(default=False)
	email = models.EmailField(unique=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name']