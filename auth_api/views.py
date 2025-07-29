from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class RegistrationView(APIView):
	"""Handles the registration post request"""

	def post(self, request):
		
		serializer = RegistrationSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			if not user:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)