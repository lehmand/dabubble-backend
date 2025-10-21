from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()

class IsOwner(permissions.BasePermission):
    """Custom Permission to only allow owners of object to edit it"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id

class IsActivated(permissions.BasePermission):
    """
    Permission to check if user has activated 
    his account via email confirmation
    """

    message = 'Your account is not activated, please check your email.'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        try:
            return request.user.user_profile.is_activated
        except UserProfile.DoesNotExist:
            return False