from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import HTTP_200_OK
from accounts.models import ConductUser, UserQuiz
from accounts.utils import Util
class ConductUserEmailView(APIView):

    queryset = ConductUser.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def post(self, request, *args, **kwargs):
        user = ConductUser.objects.get(id=self.request.user.id)
          
        if user.is_active:
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
                {"success": "We have sent you a link to reset your password"},
                status=HTTP_200_OK
            )
        else:
            return Response(
                {
                    "status": "couldn't send email",
                }
            )
        
class UserEmailView(APIView):
    queryset = UserQuiz.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
  

    def post(self, request, *args, **kwargs):
        user = ConductUser.objects.get(id=self.request.user.id)
        if user.is_active:
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
                {"success": "We have sent you a link to reset your password"},
                status=HTTP_200_OK
            )
        else:
            return Response(
                {
                    "status": "couldn't send email",
                }
            )