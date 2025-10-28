from rest_framework import serializers
from .models import Channel

class BasicChannelListSerializer(serializers.ModelSerializer):
    """Serializer for basic channel list"""

    class Meta:
        model = Channel
        fields = ['id', 'name']