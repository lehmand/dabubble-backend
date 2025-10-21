from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response

User = get_user_model()

class CurrentUserSerializer(serializers.ModelSerializer):
    """Serializer returns UserProfile"""

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer returns userprofile info from current user"""

    class Meta:
        model = UserProfile
        fields = '__all__'

class UpdateUserSerializer(serializers.ModelSerializer):
    """Serializer for CRUD operations"""

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']

    def update(self, instance, validated_data):
        """Updates the current user profile object"""
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class UpdateProfileSerializer(serializers.ModelSerializer):
    """Serializer for CRUD operations on profile from current user"""
    
    class Meta:
        model = UserProfile
        fields = ['avatar_url', 'bio']

    def update(self, instance, validated_data):
        """Update logic for userprofile of current user"""

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
