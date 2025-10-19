from django.db.models.base import post_save
from django.dispatch import receiver
from django.conf import settings
from user_profile_api.models import UserProfile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(instance)
