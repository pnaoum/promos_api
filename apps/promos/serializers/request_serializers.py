from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from apps.promos.constants import PROMO_CODE, POINTS
from apps.users.constants import ADMIN_USER, USER
from apps.users.models import UserPromos


class AssignPromoRequestSerializer(serializers.Serializer):
    promo_code = serializers.CharField()


class UserPromoRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPromos
        fields = (USER, PROMO_CODE)

    def create(self, validated_data):
        # Add total amount of promo to user points when promo is added first time
        validated_data[POINTS] = validated_data[PROMO_CODE].amount
        return super(UserPromoRequestSerializer, self).create(validated_data)

    def validate(self, attrs):
        # Reject admins to have promos
        if attrs[USER].role == ADMIN_USER:
            raise PermissionDenied('Admin users are not allowed to have promos.')
        return super(UserPromoRequestSerializer, self).validate(attrs)
