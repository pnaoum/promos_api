from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from apps.promos.models import Promo
from apps.users.constants import USER, ADMIN_USER


class PromoRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = '__all__'

    def validate(self, attrs):
        # Reject admins to have promos
        if attrs[USER].role == ADMIN_USER:
            raise PermissionDenied('Admin users are not allowed to have promos.')
        return super(PromoRequestSerializer, self).validate(attrs)


