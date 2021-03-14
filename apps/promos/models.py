from django.db import models

from apps.promos.managers import PromoManager


class Promo(models.Model):
    promo_code = models.CharField(max_length=255, unique=True)
    amount = models.PositiveIntegerField()
    type = models.CharField(max_length=10)
    creation_time = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    is_active = models.BooleanField()
    description = models.TextField()
    objects = PromoManager()
