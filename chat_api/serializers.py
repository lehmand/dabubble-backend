from rest_framework import serializers
from .models import Channel


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