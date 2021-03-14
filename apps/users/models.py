from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.users.constants import CUSTOM_USER_CHOICES, NORMAL_USER
from apps.users.managers import CustomUserManager


class CustomUser(AbstractUser):
    role = models.CharField(max_length=10, choices=CUSTOM_USER_CHOICES, default=NORMAL_USER)
    address = models.CharField(max_length=255, null=True)
    mobile_number = models.CharField(max_length=255, null=True)
    objects = CustomUserManager()
