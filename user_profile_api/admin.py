from django.contrib import admin
from .models import UserProfile

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile

    list_display = ['user', 'is_activated', 'is_guest']
