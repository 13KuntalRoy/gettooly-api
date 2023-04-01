from rest_framework.generics import (
    UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import UserQuiz, ConductUser
from accounts.serializers import (
    UserChangePasswordSerializer, ConductUserChangePasswordSerializer)
from rest_framework.response import Response
from rest_framework import status

class UserChangePasswordView(UpdateAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = UserQuiz.objects.all()
    serializer_class = UserChangePasswordSerializer
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        old_password = serializer.validated_data.get('old_password')
        password = serializer.validated_data.get('password')
        
        if not user.check_password(old_password):
            return Response({'old_password': 'Incorrect password.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(password)
        user.save()
        
        return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)


class ConductUserChangePasswordView(UpdateAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = ConductUser.objects.all()
    serializer_class = ConductUserChangePasswordSerializer
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        old_password = serializer.validated_data.get('old_password')
        password = serializer.validated_data.get('password')
        
        if not user.check_password(old_password):
            return Response({'old_password': 'Incorrect password.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(password)
        user.save()
        
        return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)