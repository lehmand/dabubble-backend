from rest_framework.views import APIView
from .serializers import CurrentUserSerializer, UpdateUserSerializer, UserProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile


class CurrentUserView(APIView):
	"""
	Handles the request for the User object
	"""

	def get(self, request):
		
		serializer = CurrentUserSerializer(request.user)
		return Response(serializer.data)
	
class UserProfileView(APIView):
	"""Handles the request for userprofile data"""

	def get(self, request):
		print('Helloworld')
		user_profile = UserProfile.objects.get(user_id=request.user.id)
		serializer = UserProfileSerializer(user_profile)
		return Response(serializer.data)

class UpdateOrDeleteCurrentUserView(APIView):
	"""
	CRUD operations on UserProfile
	"""

	def patch(self, request):
		"""
		Updates own user profile
		"""

		serializer = UpdateUserSerializer(request.user, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request):
		"""
		Deletes own user profile
		"""
		
		user = request.user
		user.delete()

		return Response({'detail': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
