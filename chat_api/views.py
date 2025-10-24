from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import BasicChannelListSerializer
from .models import Channel

# Create your views here.

class BasicChannelListView(APIView):
    """Returns the basic channel list"""

    def get(self, request):
        all_channels = Channel.objects.all()
        serializer = BasicChannelListSerializer(all_channels, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)