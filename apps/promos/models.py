from django.db import models
from django.db.models import CASCADE

from apps.promos.managers import PromoManager
from apps.users.models import CustomUser


class Promo(models.Model):
    promo_code = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=CASCADE)
    points = models.PositiveIntegerField()
    type = models.CharField(max_length=10)
    creation_time = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    is_active = models.BooleanField()
    description = models.TextField()
    objects = PromoManager()
