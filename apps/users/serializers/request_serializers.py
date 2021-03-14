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

    def validate(self, attrs):
        """
        Validate password as per AUTH_PASSWORD_VALIDATORS in settings
        """
        from django.contrib.auth.password_validation import validate_password
        validate_password(attrs['password'])
        return super(SignupSerializer, self).validate(attrs)

    def create(self, validated_data):
        """
        set_password is used to hash password in database
        """
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginRequestSerializer(serializers.Serializer):
    """
    Serializer created mainly for swagger documentation
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
