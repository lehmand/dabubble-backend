from django.db import models
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class UserProfile(models.Model):
    """Userprofile extending User Model with additional infos"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_profile'
    )
    avatar_url = models.URLField(blank=True, null=True)
    last_seen = models.DateTimeField(default=timezone.now)
    is_activated = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, default='Write something about yourself...')

    def __str__(self):
        return f"{self.user}"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def auto_create_profile(sender, instance, created, **kwargs):
    if created:
        from user_profile_api.models import UserProfile
        UserProfile.objects.create(user=instance)