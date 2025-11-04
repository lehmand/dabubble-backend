from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import BasicChannelListSerializer, CreateChannelSerializer, DetailChannelSerializer
from .models import Channel

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
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateChannelMemberView(APIView):
    pass