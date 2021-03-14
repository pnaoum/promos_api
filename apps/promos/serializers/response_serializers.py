from rest_framework import serializers

from apps.promos.models import Promo


class PromoResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        exclude = ('id',)


class UserPromoResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        exclude = ('id', 'user',)


class PointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = ('points',)
