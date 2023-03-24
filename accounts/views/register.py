from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import ConductUser, UserQuiz
from accounts.serializers import (
    UserDetailSerializer, UserRegisterSerializer, ConductUserDetailSerializer,
    ConductUserRegisterSerializer,)
from accounts.utils import Util


class UserRegisterView(CreateAPIView):
    queryset = UserQuiz.objects.all()
    permission_classes = [AllowAny,]
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            token = RefreshToken.for_user(user).access_token
            current_site = "localhost:3000"
            relative_link = reverse("email_verify")

            absurl = "http://" + current_site + \
                relative_link + "?token=" + str(token)
            email_body = "Hi " + user.first_name + \
                " use link below to verify your email\n" + absurl
            data = {
                "to_email": user.email,
                "email_subject": "Verify your email",
                "email_body": email_body,
            }
            Util.send_email(data)

            return Response(
                {
                    "user": UserDetailSerializer(
                        user, context=self.get_serializer_context()
                    ).data,
                    "status": "Successfully created User account",
                }
            )
        else:
            return Response(
                {
                    "status": "couldn't create User account",
                }
            )


class ConductUserRegisterView(CreateAPIView):

    queryset = ConductUser.objects.all()
    
    serializer_class = ConductUserRegisterSerializer
    permission_classes = [AllowAny,]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            token = RefreshToken.for_user(user).access_token
            current_site = "localhost:3000"
            relative_link = reverse("email_verify")

            absurl = "http://" + current_site + \
                relative_link + "?token=" + str(token)
            email_body = "Hi " + user.name + \
                " use link below to verify your email\n" + absurl
            data = {
                "to_email": user.email,
                "email_subject": "Verify your email",
                "email_body": email_body,
            }
            Util.send_email(data)

            return Response(
                {
                    "user": ConductUserDetailSerializer(
                        user, context=self.get_serializer_context()
                    ).data,
                    "status": "Successfully created ConductUser account",
                }
            )
        else:
            return Response(
                {
                    "status": "couldn't create ConductUser account",
                }
            )