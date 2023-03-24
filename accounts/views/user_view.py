from rest_framework.generics import (
    RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import UserQuiz, ConductUser
from accounts.serializers import (
    UserDetailSerializer, ConductUserDetailSerializer)


class UserViewSet(RetrieveAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDetailSerializer
    queryset = UserQuiz.objects.all()
    lookup_field = "id"


class ConductUserViewSet(RetrieveAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ConductUserDetailSerializer
    queryset = ConductUser.objects.all()
    lookup_field = "id"