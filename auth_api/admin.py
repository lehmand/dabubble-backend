from django.contrib import admin
from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    
    list_display = ['email', 'first_name', 'last_name', 'username', 'is_staff', 'is_superuser']