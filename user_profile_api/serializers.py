from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response

User = get_user_model()

class CurrentUserSerializer(serializers.ModelSerializer):
    """Serializer returns UserProfile"""

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class UpdateUserSerializer(serializers.ModelSerializer):
    """Serializer for CRUD operations"""

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']

    def update(self, instance, validated_data):
        """Updates the current user profile object"""
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
