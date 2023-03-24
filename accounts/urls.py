from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from accounts.views.logout import APILogoutView
from accounts.views.password_change import (
    UserChangePasswordView, ConductUserChangePasswordView)
from accounts.views.password_change_Emails import (
    EmailResetPassword, PasswordTokenCheckAPI, SetNewPasswordAPIView)
from accounts.views.register import UserRegisterView, ConductUserRegisterView
from accounts.views.token_obtain import MyObtainTokenPairView
from accounts.views.update_profile import (
    UserUpdateProfileView, ConductUserUpdateProfileView)
from accounts.views.user_view import UserViewSet, ConductUserViewSet
from accounts.views.verify_email import VerifyEmail

urlpatterns = [
    path(
        "auth/login/token/", MyObtainTokenPairView.as_view(), name="token_obtain_pair"
    ),
    path("auth/login/token/refresh/",
         TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/login/token/verify/",
         TokenVerifyView.as_view(), name="token_verify"),
    path("auth/logout/", APILogoutView.as_view(), name="logout"),
    path("auth/User/register/", UserRegisterView.as_view(), name="create-User"),
    path("auth/ConductUser/register/", ConductUserRegisterView.as_view(), name="create-ConductUser"),
    path("auth/User/change-password/<int:pk>/",
         UserChangePasswordView.as_view(), name="change-password-User"),
    path("auth/ConductUser/change-password/<int:pk>/",
         ConductUserChangePasswordView.as_view(), name="change-password-ConductUser"),
    path("User/update-profile/<int:pk>/",
         UserUpdateProfileView.as_view(), name="update-profile-User"),
    path("ConductUser/update-profile/<int:pk>/",
         ConductUserUpdateProfileView.as_view(), name="update-profile-ConductUser"),
    path("User/user/<id>", UserViewSet.as_view(), name="User-user"),
    path("ConductUser/user/<id>", ConductUserViewSet.as_view(), name="ConductUser-user"),
    path("auth/user/email-veryfy/", VerifyEmail.as_view(), name="email_verify"),
    path("auth/user/email/request-reset/",
         EmailResetPassword.as_view(), name="request-email-reset"),
    path("auth/user/email/password-reset/<uidb64>/<token>/",
         PasswordTokenCheckAPI.as_view(), name="password-reset-confirm"),
    path("auth/user/email/password-reset-complete/",
         SetNewPasswordAPIView.as_view(), name="password-reset-complete"),
]