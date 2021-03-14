from rest_framework.generics import ListCreateAPIView, GenericAPIView
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated

from apps.promos.constants import PROMO_CODE
from apps.promos.filters import PromoFilter
from apps.promos.models import Promo
from apps.promos.serializers import PromoResponseSerializer, PromoRequestSerializer
from apps.users.permissions import IsAdmin
from commons.pagination import CustomLimitOffsetPagination


class PromoListCreateView(ListCreateAPIView):
    """
    List & Create Promos - Accessible by Admins only
    """
    queryset = Promo.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin)
    pagination_class = CustomLimitOffsetPagination
    filterset_class = PromoFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PromoResponseSerializer
        else:
            return PromoRequestSerializer


class PromoUpdateDestroyView(UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Promo.objects.all()
    lookup_url_kwarg = PROMO_CODE
    lookup_field = PROMO_CODE
    serializer_class = PromoRequestSerializer
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
