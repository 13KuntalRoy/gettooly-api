from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.models import ConductUser
from accounts.serializers import ConductUserSerializer

class ConductUserSciAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
    def put(self, request, pk):
        try:
            user = ConductUser.objects.get(id=self.request.user.id)
        except ConductUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        user.stripe_customer_id = None
        user.save()
        
        serializer = ConductUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
