from rest_framework import serializers

from apps.users.constants import NORMAL_USER
from apps.users.models import CustomUser


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'role', 'address', 'mobile_number')
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True},
            'role': {'default': NORMAL_USER},
            'address': {'allow_null': True, 'required': False},
            'mobile_number': {'allow_null': True, 'required': False},
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
