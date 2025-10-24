from rest_framework import serializers
from .models import Channel

class BasicChannelListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        fields = ['id', 'name']