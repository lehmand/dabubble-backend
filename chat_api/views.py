from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import BasicChannelListSerializer, CreateChannelSerializer, DetailChannelSerializer, ManageChannelMemberSerializer, ChannelMessageSerializer, EditChannelMessageSerializer, DetailDMConversationSerializer, DMMessageSerialzer, ThreadReplySerializer
from .models import Channel, ChannelMembership, Message, DMConversation
from .permissions import IsOwner

# Create your views here.


class CreateChannelView(APIView):
    """Creating a Channel"""

    def post(self, request):
        channel_name = request.data.get('name')        
        if Channel.objects.filter(name=channel_name).exists():
            return Response({'message': 'Channel already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CreateChannelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BasicChannelListView(APIView):
    """Returns the basic channel list"""

    def get(self, request):
        all_channels = Channel.objects.all()
        serializer = BasicChannelListSerializer(all_channels, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class DetailChannelView(APIView):
    """CRUD for detail channel view"""

    def get(self, request, pk):
        """Get all data to display channel with members and messages"""
        try:
            channel = Channel.objects.prefetch_related(
                'members__user_profile',
                'created_by__user_profile'
            ).get(pk=pk)
        except Channel.DoesNotExist:
            return Response(
                {'message': 'Channel not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = DetailChannelSerializer(channel)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        """Patch the channel name and/or description"""
        try:
            channel = Channel.objects.get(pk=pk)
        except Channel.DoesNotExist:
            return Response(
                {'message': 'Channel not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = DetailChannelSerializer(channel, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'id': channel.id,
                'name': channel.name,
                'description': channel.description
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateChannelMemberView(APIView):
    """Adds or removes members from channel"""

    def post(self, request, pk):
        try:
            channel = Channel.objects.get(pk=pk)
        except Channel.DoesNotExist:
            return Response('Channel not found!', status=status.HTTP_400_BAD_REQUEST)

        serializer = ManageChannelMemberSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_ids = serializer.validated_data['user_ids']
        action = serializer.validated_data['action']

        if action == 'add':
            added_count = 0
            for user_id in user_ids:
                _, created = ChannelMembership.objects.get_or_create(
                    channel=channel,
                    user_id=user_id
                )
                if created:
                    added_count +=1
            return Response({
                'message': f'Added {added_count} members to channel.',
                'channel_id': channel.id
            }, status=status.HTTP_200_OK)

        elif action == 'remove':
            removed_counter = ChannelMembership.objects.filter(
                channel=channel,
                user_id__in=user_ids
            ).delete()[0]

            return Response({
                'message': f'{removed_counter} members removed from channel',
                'channel_id': channel.id
            }, status=status.HTTP_200_OK)


class ChannelMessageView(APIView):
    """
    Channel message view for
    posting, deleting and editing channel messages
    """
    def post(self, request, pk):
        """Handler for posting channel messages"""
        serializer = ChannelMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                    sender=request.user,
                    channel_id=pk
                    )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk):
        """Get all channel messages"""
        messages = Message.objects.filter(channel_id=pk).order_by('created_at')
        serializer = ChannelMessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EditChannelMessage(APIView):
    """View for editing and delete messages"""

    permission_classes = [IsOwner]

    def patch(self, request, pk):
        message = Message.objects.get(pk=pk)

        self.check_object_permissions(request, message)

        serializer = EditChannelMessageSerializer(message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk):
        """Deletes channel message"""
        message = Message.objects.get(pk=pk)
        self.check_object_permissions(request, message)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetOrCreateDmConversationView(APIView):
    """Get an existing DM conversation or create one"""

    def get(self, request, user_id):
        from django.db.models import Q
        from django.contrib.auth import get_user_model

        User = get_user_model()

        try:
            other_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.id == user_id:
            dm_conversation = DMConversation.objects.filter(
                    user_1=request.user,
                    user_2=request.user
                    ).first()

            if not dm_conversation:
                dm_conversation = DMConversation.objects.create(
                        user_1=request.user,
                        user_2=request.user
                        )

        else:
            dm_conversation = DMConversation.objects.filter(
                    Q(user_1=request.user, user_2=user_id) |
                    Q(user_2=user_id, user_1=request.user)
                    ).first()

            if not dm_conversation:
                dm_conversation = DMConversation.objects.create(
                        user_1=request.user,
                        user_2=other_user
                        )

        serializer = DetailDMConversationSerializer(dm_conversation)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DMMessageView(APIView):
    """Methods for posting, editing and deleting dm messages"""
        
    def post(self, request, dm_conversation_id):
        """Method for creating dm messages"""
        try:
            dm_conversation = DMConversation.objects.get(pk=dm_conversation_id)
        except DMConversation.DoesNotExist:
            return Response({'message': 'dm conversation not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in [dm_conversation.user_1, dm_conversation.user_2]:
            return Response({'message': 'Your are not part of this conversation'}, status=status.HTTP_403_FORBIDDEN)

        serializer = DMMessageSerialzer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                    sender=request.user,
                    dm_conversation=dm_conversation
                    )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.status.HTTP_400_BAD_REQUEST)


class EditDMMessage(APIView):
    """Delete and editing dm messages"""
    permission_classes = [IsOwner]
    def patch(self, request, pk):
        """Editing DM messages"""
        try:
            message = Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            return Response({'message': 'message not found'})

        self.check_object_permissions(request, message)
        serializer = DMMessageSerialzer(message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """Deleting DM messages"""
        try:
            message = Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            return Response({'message': 'message not found'})

        self.check_object_permissions(request, message)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ThreadReplyView(APIView):
    """Create, edit and delete thread reply messages"""
    
    def post(self, request, message_id):
        """Create thread message"""
        try:
            message = Message.objects.get(pk=message_id)
        except Message.DoesNotExist:
            return Response({'message': 'message not found'})

        serializer = ThreadReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                    sender=request.user,
                    parent_message=message
                    )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
