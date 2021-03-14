from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.promos.constants import POINTS, ERR_MSG_POINTS_POSITIVE, ERR_MSG_ADMIN_NO_PROMO, END_TIME, START_TIME, \
    ERR_MSG_END_TIME_BIGGER
from apps.promos.models import Promo
from apps.users.constants import USER, ADMIN_USER


class PromoRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = '__all__'

    def validate(self, attrs):
        # Assert points are positive
        if attrs[POINTS] < 0:
            raise ValidationError(ERR_MSG_POINTS_POSITIVE)
        if END_TIME in attrs and attrs[END_TIME]:
            if attrs[END_TIME] < attrs[START_TIME]:
                raise ValidationError(ERR_MSG_END_TIME_BIGGER)
        # Reject admins to have promos
        if attrs[USER].role == ADMIN_USER:
            raise PermissionDenied(ERR_MSG_ADMIN_NO_PROMO)
        return super(PromoRequestSerializer, self).validate(attrs)
