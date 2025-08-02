from rest_framework.views import APIView
from .serializers import CurrentUserSerializer
from rest_framework.response import Response


class CurrentUserView(APIView):
	"""Handles the request for the User object"""

	def post(self, request):
		
		serializer = CurrentUserSerializer(request.user)
		return Response(serializer.data)