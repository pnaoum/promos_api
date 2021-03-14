from django.views.generic import detail
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.promos.constants import PROMO_CODE
from apps.promos.filters import PromoFilter
from apps.promos.models import Promo
from apps.promos.serializers import PromoSerializer, UserPromoRequestSerializer, AssignPromoRequestSerializer
from apps.users.constants import USER, USER_ID
from apps.users.permissions import IsAdmin
from commons.global_constants import DETAIL, BAD_REQUEST
from commons.pagination import CustomLimitOffsetPagination


class PromoListCreateView(ListCreateAPIView):
    """
    List & Create Promos - Accessible by Admins only
    """
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    pagination_class = CustomLimitOffsetPagination
    filterset_class = PromoFilter


class PromoUpdateDestroyView(UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Promo.objects.all()
    lookup_url_kwarg = PROMO_CODE
    lookup_field = PROMO_CODE
    serializer_class = PromoSerializer
    permission_classes = (IsAuthenticated, IsAdmin)

    def put(self, request, *args, **kwargs):
        """
        Edit Promo - Accessible by Admins only
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Delete Promo - Accessible by Admins only
        """
        return self.destroy(request, *args, **kwargs)


class AssignPromoView(APIView):
    permission_classes = (IsAuthenticated, IsAdmin)

    @swagger_auto_schema(request_body=AssignPromoRequestSerializer)
    def post(self, request, *args, **kwargs):
        """
        Assign promo to user - Accessible by Admins only
        """
        data = request.data.copy()
        data[USER] = self.kwargs[USER_ID]
        serializer = UserPromoRequestSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={DETAIL: BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        # except ValidationError as v:
        #     return Response(data=v, status=status.HTTP_400_BAD_REQUEST)
        # except Exception as e:
        #     from config.loggers import log_exception
        #     log_exception(e)
        #     return Response(data=BAD_REQUEST, status=status.HTTP_400_BAD_REQUEST)
