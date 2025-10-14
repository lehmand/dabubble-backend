from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for the registration view"""
    
    repeated_password = serializers.CharField(write_only=True)
    name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'name', 'first_name', 'last_name', 'email', 'password', 'repeated_password', 'avatar_url']
        extra_kwargs = {'password': {'write_only': True}}

    def __init__(self, *args, **kwargs):
        """Transforms initial data from JSON format to snake_case
        
        Note: This is done manually on purpose for practice reasons
        There is a third party package available for this procedure."""

        if 'data' in kwargs:
            data = kwargs['data']
            new_data = data.copy()

            if 'repeatedPassword' in data:
                new_data['repeated_password'] = data['repeatedPassword']
            
            if 'avatarUrl' in data:
                new_data['avatar_url'] = data['avatarUrl']

            kwargs['data'] = new_data
        super().__init__(*args, **kwargs)

    def validate_email(self, value):
        """Validate the email and checks if email already in use"""

        users = User.objects.all()
        user_email = users.filter(email=value)

        if user_email:
            raise serializers.ValidationError({'message': 'Email already in use!'})
        return value
    
    def validate(self, data):
        """Validates the password and checks if both passwords matches."""

        if len(data['password']) < 8:
            raise serializers.ValidationError({'message': 'Password too short, min 8 chars!'})
        
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({'message': 'Passwords don\'t match!'})
        
        return data
    
    def create(self, validated_data):
        """Create user in the database and returns it"""

        validated_data.pop('repeated_password')
        password = validated_data.pop('password')
        name_parts = validated_data['name'].strip().split()
        first_name = name_parts[0]
        last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
        username = validated_data.get('email').split('@')[0]

        user = User(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = validated_data['email'],
            avatar_url = validated_data['avatar_url']
        )


        user.set_password(password)
        user.save()

        return user
    
    def to_representation(self, instance):
        """Transforms snake_case format to JSON for the frontend

        Note: This is done manually on purpose for practice reasons
        There is a third party package available for this procedure.        
        """        
            
        rep = super().to_representation(instance)

        return {
            'id': rep['id'],
            'firstName': rep['first_name'],
            'lastName': rep['last_name'],
            'email': rep['email'],
            'avatarUrl': rep['avatar_url']
        }
