from rest_framework import serializers

from apps.promos.constants import POINTS
from apps.promos.models import Promo
from apps.users.constants import USER


class PromoResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        exclude = ('id',)  # promo_code is the unique identifier exposed to the users, id is not exposed


class UserPromoResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        exclude = ('id', USER,)  # users by default retrieve their data, user id is not exposed


class PointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = (POINTS,)
