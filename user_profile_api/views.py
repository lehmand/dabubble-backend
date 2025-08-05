from rest_framework.views import APIView
from .serializers import CurrentUserSerializer, UpdateOrDeleteCurrentUserSerializer
from rest_framework.response import Response
from rest_framework import status


class CurrentUserView(APIView):
	"""
	Handles the request for the User object
	"""

	def post(self, request):
		
		serializer = CurrentUserSerializer(request.user)
		return Response(serializer.data)
	

class UpdateOrDeleteCurrentUser(APIView):
	"""
	CRUD operations on UserProfile
	"""

	def patch(self, request):
		"""
		Updates own user profile
		"""

		serializer = UpdateOrDeleteCurrentUserSerializer(request.user, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request):
		"""
		Deletes own user profile
		"""
		
		user = request.user
		user.delete()

		return Response({'detail': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)