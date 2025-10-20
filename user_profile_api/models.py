from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_profile'
    )
    avatar_url = models.URLField(blank=True, null=True)
    last_seen = models.DateTimeField(default=timezone.now)
    is_activated = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.user}"
