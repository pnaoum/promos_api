from rest_framework import serializers

from apps.promos.constants import PROMO_CODE, POINTS
from apps.promos.models import Promo
from apps.users.models import UserPromos


class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        exclude = ('id',)


class UserPromoResponseSerializer(serializers.ModelSerializer):
    # promo = PromoSerializer(source='promo_code')  # Serialize full promo object
    promo_code = serializers.CharField(read_only=True, source='promo_code.promo_code')

    class Meta:
        model = UserPromos
        fields = (PROMO_CODE, POINTS)
