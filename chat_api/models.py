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

    def save(self, *args, **kwargs):
        """Gives creator of channel admin role"""

        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and self.created_by:
            ChannelMembership.get_or_create(
                channel=self,
                user=self.created_by,
                defaults={'role': 'admin'}
            )

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
    role = models.CharField(
        max_length=20,
        choices=[
            ('admin', 'Admin'),
            ('member', 'Member')
        ],
        default='member'
    )

    class Meta:
        unique_together = ['channel', 'user']

    def __str__(self):
        return f"User {self.user} joined {self.channel} at {self.joined_at}"


class DMConversation(models.Model):
    user_1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dm_conversation_as_user1'
    )
    user_2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dm_conversation_as_user2'
    )
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    text = models.TextField(blank=False, max_length=500)
    is_edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name='messages',
        null=True,
        blank=True
    )
    dm_conv = models.ForeignKey(
        DMConversation,
        on_delete=models.CASCADE,
        related_name='messages',
        null=True,
        blank=True
    )
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='thread_replies',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        channel_name = self.channel.name if self.channel else 'DM/Thread'
        return f"{self.sender.first_name}: {self.text[:10]} -> {channel_name}"
