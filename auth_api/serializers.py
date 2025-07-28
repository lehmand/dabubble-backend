from rest_framework import serializers
from django.conf import settings

class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for the registration view"""
    
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
