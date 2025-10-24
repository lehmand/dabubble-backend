from django.contrib import admin
from .models import Channel

# Register your models here.
@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    model = Channel

    list_display = ['name', 'description', 'created_by', 'created_at']