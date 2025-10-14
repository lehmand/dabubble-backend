from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response

User = get_user_model()

class CurrentUserSerializer(serializers.ModelSerializer):
    """Serializer returns User object for token"""

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'date_joined', 'avatar_url', 'is_online', 'is_activated']

    def to_representation(self, instance):
        """Tranforms snake_case to JSON format

        Note: This is done manually on purpose for practice reason
        There is a third party package available for this procedure.
        """

        rep = super().to_representation(instance)

        return {
            'id': rep['id'],
            'firstName': rep['first_name'],
            'lastName': rep['last_name'],
            'email': rep['email'],
            'dateJoined': rep['date_joined'],
            'avatarUrl': rep['avatar_url'],
            'isOnline': rep['is_online'],
            'isActivated': rep['is_activated']
        }
    
class UpdateOrDeleteCurrentUserSerializer(serializers.ModelSerializer):
    """Serializer for CRUD operations"""

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'avatar_url']

    def __init__(self, *args, **kwargs):
        """
        Transform JSON data to snake_case

        Note: This is done manually on purpose for practice reason
        There is a third party package available for this procedure.
        """

        if 'data' in kwargs:
            initial_data = kwargs['data']
            new_data = initial_data.copy()

            if 'firstName' in initial_data:
                new_data['first_name'] = initial_data['firstName']

            if 'lastName' in initial_data:
                new_data['last_name'] = initial_data['lastName']

            if 'avatarUrl' in initial_data:
                new_data['avatar_url'] = initial_data['avtarUrl']

            kwargs['data'] = new_data
        super().__init__(*args, **kwargs)


    def update(self, instance, validated_data):
        """
        Updates the current user object
        """
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    
    def to_representation(self, instance):
        """
        Transforms snake_case to JSON format

        Note: This is done manually on purpose for practice reason
        There is a third party package available for this procedure.
        """

        resp = super().to_representation(instance)

        return {
            'id': resp['id'],
            'firstName': resp['first_name'],
            'lastName': resp['last_name'],
            'email': resp['email'],
            'avatarUrl': resp['avatar_url']
        }
