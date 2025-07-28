from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class RegistrationView(APIView):
	"""Handles the registration post request"""

	def post(self, request):
		pass