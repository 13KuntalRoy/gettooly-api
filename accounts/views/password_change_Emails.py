from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import ValidationError

from django.urls import reverse
from django.utils.encoding import (
    DjangoUnicodeDecodeError, smart_bytes, smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from accounts.models import CustomUser
from accounts.serializers import EmailResetPasswordSerializer, SetNewPasswordSerializer
from accounts.utils import Util
from django.forms.models import model_to_dict
from django.utils.encoding import force_str


class EmailResetPassword(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EmailResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            if CustomUser.objects.filter(email=email).exists():
                user = CustomUser.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                current_site = "localhost:3000"
                relative_link = reverse(
                    "password-reset-confirm", kwargs={'uidb64': uidb64, 'token': token})

                absurl = "http://" + current_site + relative_link
                email_body = "Hello \n Use link below to reset your password\n" + absurl
                data = {
                    "to_email": user.email,
                    "email_subject": "Reset your password",
                    "email_body": email_body,
                }
                Util.send_email(data)

                return Response(
                    {"success": "We have sent you a link to reset your password"},
                    status=HTTP_200_OK
                )

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class PasswordTokenCheckAPI(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {"error": "Token is not valid, please request a new one"},
                    status=HTTP_401_UNAUTHORIZED
                )

            return Response(
                {
                    "success": True,
                    "message": "Credential valid",
                    "uidb64": uidb64,
                    "token": token
                },
                status=HTTP_200_OK
            )

        except (DjangoUnicodeDecodeError, CustomUser.DoesNotExist):
            return Response(
                {"error": "Token is not valid, please request a new one"},
                status=HTTP_401_UNAUTHORIZED
            )
class SetNewPasswordAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data.get("password")
            uidb64 = serializer.validated_data.get("uidb64")
            token = serializer.validated_data.get("token")
            
            if not uidb64:
                return Response(
                    {"error": "uidb64 parameter is missing or empty"},
                    status=HTTP_400_BAD_REQUEST
                )

            try:
                id = force_str(urlsafe_base64_decode(uidb64))
                user = CustomUser.objects.get(id=id)
                

                if not PasswordResetTokenGenerator().check_token(user, token):

                    return Response(
                        {"error": "Token is not valid, please request a new one"},
                        status=HTTP_401_UNAUTHORIZED
                    )
                
                user.set_password(password)
                user.save()
                access_token = RefreshToken.for_user(user).access_token

                return Response(
                    {
                        "success": True,
                        "message": "Password reset success",
                        "access_token": str(access_token)
                    },
                    status=HTTP_200_OK
                )

            except (TypeError, ValueError, OverflowError, UnicodeDecodeError, CustomUser.DoesNotExist):
                return Response(
                    {"error": "Invalid or expired reset link"},
                    status=HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
