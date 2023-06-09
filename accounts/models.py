import datetime

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from accounts.managers import CustomUserManager

TYPE_CHOICES = (
    (1, _("ConductUser")),
    (2, _("UserQuiz")),
)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)

    phone_number = PhoneNumberField()

    country = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    pin = models.PositiveIntegerField(null=True)

    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    type = models.IntegerField(choices=TYPE_CHOICES, default=1)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class ConductUser(CustomUser):

    name = models.CharField(max_length=30)
    profile_photo = models.ImageField(
        upload_to="media/images", null=True, default=""
    )


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Quiz Conduct User"


GENDER_CHOICES = [("Male", "Male"), ("Female", "Female"), ("Others", "Others")]


class UserQuiz(CustomUser):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    gender = models.CharField(
        max_length=100, choices=GENDER_CHOICES, default=1
    )
    DOB = models.DateField(_("DOB"), default=datetime.date.today)
    profile_photo = models.ImageField(
        upload_to="media/images", null=True, default=""
    )

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = "Quiz Give User"