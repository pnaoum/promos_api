from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.users.constants import CUSTOM_USER_CHOICES, NORMAL_USER
from apps.users.managers import CustomUserManager


class CustomUser(AbstractUser):
    role = models.CharField(max_length=10, choices=CUSTOM_USER_CHOICES, default=NORMAL_USER)
    address = models.CharField(max_length=255, null=True)
    mobile_number = models.CharField(max_length=255, null=True)
    objects = CustomUserManager()

#
# class UserPromos(models.Model):
#     """
#     MTM table for user - promo relationship
#     """
#     user = models.ForeignKey(CustomUser, on_delete=CASCADE)
#     promo_code = models.ForeignKey(Promo, on_delete=CASCADE, to_field=PROMO_CODE, db_column=PROMO_CODE)
#     points = models.PositiveIntegerField()
#
#     class Meta:
#         unique_together = (USER, PROMO_CODE)
