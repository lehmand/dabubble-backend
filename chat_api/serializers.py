from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta
from .models import Channel, Message
from user_profile_api.serializers import NestedProfileInfoSerializer
from django.contrib.auth import get_user_model
from django.utils import timezone

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


class ManageChannelMemberSerializer(serializers.Serializer):
    """Adds and remove channel members"""

    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True
    )

    action = serializers.ChoiceField(
        choices=['add', 'remove'],
        required=True
    )

    def validate_user_ids(self, value):
        """Checks if all ids exists"""
        if not value:
            raise serializers.ValidationError('At least one id must be given.')

        existing_ids = User.objects.filter(id__in=value).values_list('id', flat=True)
        missing_ids = set(value) - set(existing_ids)

        if missing_ids:
            raise serializers.ValidationError(f"Users with the ids {missing_ids} does not exist.")

        return value


class ChannelMessageSerializer(serializers.ModelSerializer):
    """Serializer for posting channel messages"""
    class Meta:
        model = Message
        fields = ['id', 'text', 'created_at'] 
        read_only_fields = ['id', 'created_at']


class DirectMessageSerializer(serializers.ModelSerializer):
    """Serializer for posting DMs"""
    class Meta:
        model = Message
        fields = ['id', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']


class ThreadMessageSerializer(serializers.ModelSerializer):
    """Serializer for posting thread messages"""
    class Meta:
        model = Message
        fields = ['id', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']


class EditChannelMessageSerializer(serializers.ModelSerializer):
    """Edit channel messages"""
    class Meta:
        model = Message
        fields = ['id', 'text', 'is_edited', 'edited_at']
        read_only_field = ['is_edited', 'edited_at']

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)         
        instance.is_edited = True
        instance.edited_at = timezone.now()
        instance.save()
        return instance
