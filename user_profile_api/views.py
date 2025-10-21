from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import UserProfile
from .serializers import CurrentUserSerializer, UpdateUserSerializer, UserProfileSerializer, UpdateProfileSerializer, UserListSerializer
from .permissions import IsOwner, IsActivated
from django.contrib.auth import get_user_model

User = get_user_model()


class CurrentUserView(APIView):
	"""Handles the request for the User object"""

	permission_classes = [IsAuthenticated, IsActivated]

	def get(self, request):
		
		serializer = CurrentUserSerializer(request.user)
		return Response(serializer.data)
	
class UserProfileView(APIView):
	"""Handles the request for userprofile data"""

	permission_classes = [IsAuthenticated, IsActivated]

	def get(self, request):
		user_profile = UserProfile.objects.get(user_id=request.user.id)
		serializer = UserProfileSerializer(user_profile)
		return Response(serializer.data)

class UpdateProfileView(APIView):
	"""Update view for the userprofile of currentuser"""

	permission_classes = [IsAuthenticated, IsOwner, IsActivated]
	
	def patch(self, request):
		profile = UserProfile.objects.get(user_id=request.user.id)
		serializer = UpdateProfileSerializer(profile, data=request.data, partial=True)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateOrDeleteCurrentUserView(APIView):
	"""CRUD operations on UserProfile"""

	permission_classes = [IsAuthenticated, IsOwner, IsActivated]

	def patch(self, request):
		"""Updates own user profile"""

		serializer = UpdateUserSerializer(request.user, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request):
		"""Deletes own user profile"""
		
		user = request.user
		user.delete()

		return Response(status=status.HTTP_204_NO_CONTENT)

class UserListView(APIView):
	"""List view of all users"""

	permission_classes = [IsAuthenticated, IsActivated]

	def get(self, request):
		queryset = User.objects.all()
		serializer = UserListSerializer(queryset, many=True)
		return Response(serializer.data)