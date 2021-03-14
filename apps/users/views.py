from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import CustomUser
from apps.users.serializers import SignupSerializer, LoginRequestSerializer, LoginResponseSerializer
from commons.global_constants import DETAIL


class SignUp(CreateAPIView):
    """
    Users Registration with username, password and role
    """
    queryset = CustomUser.objects.all()
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        response = super(SignUp, self).post(request, *args, **kwargs)
        if response.status_code == 201:
            return Response(data={'detail': 'Ok'}, status=status.HTTP_201_CREATED)
        return response


class Login(APIView):
    """
    Users Login with username and password

    returns: Token to be used afterwards
    """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=LoginRequestSerializer,
                         responses={200: openapi.Response('Ok', LoginResponseSerializer)})
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user:
            token, c = Token.objects.get_or_create(user=user)
            if token:
                return Response(data={'token': token.key}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={DETAIL: 'Invalid credentials.'})
