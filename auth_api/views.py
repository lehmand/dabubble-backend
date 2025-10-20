from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from .utils import create_activation_link, send_activation_email
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user_profile_api.models import UserProfile

User = get_user_model()

# Create your views here.
class RegistrationView(APIView):
	"""Handles the registration post request"""

	def post(self, request):
		
		serializer = RegistrationSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			activation_link = create_activation_link(user)
			send_activation_email(user.email, user.first_name, activation_link)
			if not user:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
class ActivationView(APIView):
	"""Handles the account activation process"""

	def get(self, request, uidb64, token):

		try:
			uid = urlsafe_base64_decode(uidb64).decode()
			user = User.objects.get(pk=uid)
		except (User.DoesNotExist):
			user = None

		success_context = {
			'success_url': 'https://dabubble.daniel-lehmann.dev/login/',
			'first_name': user.first_name
		}

		if user is not None and default_token_generator.check_token(user, token):
			userprofile = UserProfile.objects.get(user_id=user.pk)
			userprofile.is_activated = True
			userprofile.save()

			return render(request, 'auth_api/redirect_pages/activation_success.html', success_context)
		else:
			return render(request, 'auth_api/redirect_pages/activation_invalid.html')


class CookieTokenObtainPairView(TokenObtainPairView):
	"""Customized View to set cookies for the access and refresh tokens"""
	serializer_class = TokenObtainPairSerializer

	def post(self, request, *args, **kwargs):
		response = super().post(request, *args, **kwargs)

		token_data = response.data
		access_token = token_data.get('access')
		refresh_token = token_data.get('refresh')

		response.set_cookie(
			key='access_token',
			value=access_token,
			httponly=True,
			secure=False,
			samesite='Lax'
		)

		response.set_cookie(
			key='refresh_token',
			value=refresh_token,
			httponly=True,
			secure=False,
			samesite='Lax'
		)

		return response
	
class CookieTokenRefreshView(TokenRefreshView):
	serializer_class = TokenRefreshSerializer

	def post(self, request, *args, **kwargs):
		response = super().post(request, *args, **kwargs)

		token_data = response.data
		access_token = token_data.get('access')

		response.set_cookie(
			key='access_token',
			value=access_token,
			httponly=True,
			secure=False,
			samesite='Lax'
		)

		return response

