from rest_framework.generics import (
    UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import UserQuiz, ConductUser
from accounts.serializers import (
    UserChangePasswordSerializer, ConductUserChangePasswordSerializer)


class UserChangePasswordView(UpdateAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = UserQuiz.objects.all()
    serializer_class = UserChangePasswordSerializer


class ConductUserChangePasswordView(UpdateAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = ConductUser.objects.all()
    serializer_class = ConductUserChangePasswordSerializer