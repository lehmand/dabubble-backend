from django.db import models
from django.conf import settings

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_profile'
    )
    avatar_url = models.URLField(blank=True, null=True)
    is_online = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    is_activated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"
