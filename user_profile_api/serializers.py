from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class CurrentUserSerializer(serializers.ModelSerializer):
    """Serializer returns User object for token"""

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'date_joined', 'avatar_url', 'is_online']

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        return {
            'id': rep['id'],
            'firstName': rep['first_name'],
            'lastName': rep['last_name'],
            'email': rep['email'],
            'dateJoined': rep['date_joined'],
            'avatarUrl': rep['avatar_url'],
            'isOnline': rep['is_online']
        }