from django.db import models
from django.conf import settings

# Create your models here.

class Channel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_channels'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ChannelMembership',
        related_name='channels'
    )

    class Meta:
        ordering = ['name']

        indexes = [
            models.Index(fields=['name'])
        ]


    def __str__(self):
        return f"Channel {self.name} created by {self.created_by}"

class ChannelMembership(models.Model):
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='channel_memberships'
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['channel', 'user']

    def __str__(self):
        return f"User {self.user} joined {self.channel} at {self.joined_at}"

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    text = models.TextField(blank=False, max_length=500)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(auto_now_add=True)
    