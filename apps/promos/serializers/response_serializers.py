from rest_framework import serializers

from apps.promos.constants import POINTS
from apps.promos.models import Promo
from apps.users.constants import USER


class PromoResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        exclude = ('id',)


class UserPromoResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        exclude = ('id', USER,)


class PointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = (POINTS,)
