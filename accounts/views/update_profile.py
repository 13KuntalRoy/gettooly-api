from rest_framework.generics import (
    UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import UserQuiz, ConductUser
from accounts.serializers import (
    UserUpdateUserSerializer, ConductUserUpdateUserSerializer)


class UserUpdateProfileView(UpdateAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = UserQuiz.objects.all()
    serializer_class = UserUpdateUserSerializer
    def perform_update(self, serializer):
        return serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer =UserUpdateUserSerializer(instance=instance, many=False)
        return Response({"data": serializer.data, "status": "Successfully updated User details"})

class ConductUserUpdateProfileView(UpdateAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = ConductUser.objects.all()
    serializer_class = ConductUserUpdateUserSerializer
    def perform_update(self, serializer):
        return serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer =ConductUserUpdateUserSerializer(instance=instance, many=False)
        return Response({"data": serializer.data, "status": "Successfully updated ConductUser details"})


       