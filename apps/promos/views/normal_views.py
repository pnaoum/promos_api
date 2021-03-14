from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.promos.constants import PROMO_CODE, POINTS
from apps.promos.filters import PromoFilter
from apps.promos.serializers import UserPromoResponseSerializer, PromoSerializer
from apps.users.models import UserPromos
from commons.pagination import CustomLimitOffsetPagination


class PromoList(ListAPIView):
    """
    List all available user's promos
    """
    serializer_class = PromoSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomLimitOffsetPagination
    filterset_class = PromoFilter

    def get_queryset(self):
        return self.request.user.promos.all()


class PromoPointsView(RetrieveModelMixin, CreateModelMixin, GenericAPIView):
    lookup_url_kwarg = PROMO_CODE
    lookup_field = PROMO_CODE
    serializer_class = UserPromoResponseSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.userpromos_set.all()

    def get(self, request, *args, **kwargs):
        """
        Retrieve user's points remaining for a promo
        """
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Deduct points from user's promo
        """
        try:
            points = request.data[POINTS]
            # Assert input is valid integer
            try:
                points = int(points)
            except ValueError:
                return Response(data={"points": "points have to be a valid integer"},
                                status=status.HTTP_400_BAD_REQUEST)
            promo_code = self.kwargs.get(PROMO_CODE, None)
            try:
                promo_set = self.request.user.userpromos_set.get(promo_code=promo_code)
                if promo_set.points < points:
                    return Response(data={POINTS: 'You do not have enough points to consume in this promo'},
                                    status=status.HTTP_400_BAD_REQUEST)
                promo_set.points -= points
                promo_set.save()
                return Response(UserPromoResponseSerializer(promo_set).data, status=status.HTTP_202_ACCEPTED)
            except UserPromos.DoesNotExist as e:
                from config.loggers import log_exception
                log_exception(e)
                return Response(data='Bad Request', status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:  # Unexpected errors
            from config.loggers import log_exception
            log_exception(e)
            return Response(data='Bad Request', status=status.HTTP_400_BAD_REQUEST)
