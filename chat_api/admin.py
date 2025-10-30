from django.contrib import admin
from .models import Channel, Message, ChannelMembership, DMConversation

# Register your models here.
@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    model = Channel

    list_display = ['name', 'description', 'created_by', 'created_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    model = Message

    list_display = ['sender', 'channel', 'text']


@admin.register(ChannelMembership)
class MembershipAdmin(admin.ModelAdmin):
    model = ChannelMembership

    list_display = ['user', 'channel', 'role']


@admin.register(DMConversation)
class DMAdmin(admin.ModelAdmin):
    model = DMConversation

    list_display = ['user_1', 'user_2']