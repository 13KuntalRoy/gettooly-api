from .base import *
from .base import env

DEBUG=True

SECRET_KEY = env("DJANGO_SECRET_KEY",default='django-insecure-2rzz_nic_()ry3174#)yo_93_u1)rt43t=-v3&03cibw(7-+rt')

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]