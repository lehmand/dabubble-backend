from rest_framework import serializers
from .models import Channel
from user_profile_api.serializers import NestedProfileInfoSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateChannelSerializer(serializers.ModelSerializer):
    """Serializer for creating channels"""

    class Meta:
        model = Channel
        fields = ['id', 'name', 'description']
        extra_kwargs = {
            'description': {'required': False}
        }

class BasicChannelListSerializer(serializers.ModelSerializer):
    """Serializer for basic channel list"""

    class Meta:
        model = Channel
        fields = ['id', 'name']


class ChannelMemberSerializer(serializers.ModelSerializer):
    """Serializer for detailed member view"""

    user_profile = NestedProfileInfoSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'user_profile']


class DetailChannelSerializer(serializers.ModelSerializer):
    """Serializer for channel detail view"""

    members = ChannelMemberSerializer(many=True, read_only=True)
    created_by = ChannelMemberSerializer(read_only=True)

    class Meta:
        model = Channel
        fields = ['id', 'name', 'description', 'created_at', 'created_by', 'members']