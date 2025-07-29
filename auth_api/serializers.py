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
        if 'data' in kwargs:
            data = kwargs['data']
            new_data = data.copy()

            if 'repeatedPassword' in data:
                new_data['repeated_password'] = data['repeatedPassword']
            
            if 'avatar' in data:
                new_data['avatar_url'] = data['avatar']

            kwargs['data'] = new_data
        super().__init__(*args, **kwargs)

    def validate_email(self, value):
        users = User.objects.all()
        user_email = users.filter(email=value)

        if user_email:
            raise serializers.ValidationError({'message': 'Email already in use!'})
        return value
    
    def validate(self, data):

        if len(data['password']) < 8:
            raise serializers.ValidationError({'message': 'Password too short, min 8 chars!'})
        
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({'message': 'Passwords don\'t match!'})
        
        return data
    
    def create(self, validated_data):
        validated_data.pop('repeated_password')
        password = validated_data.pop('password')
        name_parts = validated_data['name'].strip().split()
        first_name = name_parts[0]
        last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

        user = User(
            first_name = first_name,
            last_name = last_name,
            email = validated_data['email'],
            avatar_url = validated_data['avatar_url']
        )


        user.set_password(password)
        user.save()

        return user