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

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"data": serializer.data, "status": "Successfully updated User details"})


class ConductUserUpdateProfileView(UpdateAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = ConductUser.objects.all()
    serializer_class = ConductUserUpdateUserSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"data": serializer.data, "status": "Successfully updated ConductUser details"})