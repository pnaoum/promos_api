from datetime import datetime

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response

from apps.promos.constants import PROMO_CODE, POINTS, ERR_MSG_POINTS_POSITIVE, ERR_MSG_NO_ENOUGH_POINTS, \
    ERR_MSG_PROMO_EXPIRED, END_TIME
from apps.promos.filters import UserPromoFilter
from apps.promos.models import Promo
from apps.promos.serializers import UserPromoResponseSerializer, PointsSerializer
from commons.global_constants import DETAIL, NOT_FOUND, BAD_REQUEST
from commons.pagination import CustomLimitOffsetPagination


class UserPromoList(ListAPIView):
    """
    List all available user's promos
    """
    serializer_class = UserPromoResponseSerializer
    pagination_class = CustomLimitOffsetPagination
    filterset_class = UserPromoFilter

    def get_queryset(self):
        return Promo.objects.filter(user=self.request.user)


class PromoPointsView(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    lookup_url_kwarg = PROMO_CODE
    lookup_field = PROMO_CODE
    serializer_class = PointsSerializer

    def get_queryset(self):
        return Promo.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        """
        Retrieve user's points for a promo
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Edit user's points for a promo by deducting points
        """
        try:
            points = request.data[POINTS]
            # Assert input is valid positive integer
            try:
                points = int(points)
                if points < 0:
                    raise ValueError
            except ValueError:
                return Response(data={POINTS: ERR_MSG_POINTS_POSITIVE}, status=status.HTTP_400_BAD_REQUEST)
            promo_code = self.kwargs.get(PROMO_CODE, None)
            try:
                promo = Promo.objects.get(promo_code=promo_code)
                # Reject operation if user consumes more points than available
                if promo.points < points:
                    return Response(data={POINTS: ERR_MSG_NO_ENOUGH_POINTS},
                                    status=status.HTTP_400_BAD_REQUEST)
                # Reject operation if current time exceeds promo end_time (i.e.: promo expired)
                if promo.end_time and promo.end_time < datetime.now():
                    return Response(data={END_TIME: ERR_MSG_PROMO_EXPIRED},
                                    status=status.HTTP_400_BAD_REQUEST)
                promo.points -= points
                promo.save()
                return Response(PointsSerializer(promo).data, status=status.HTTP_202_ACCEPTED)
            except Promo.DoesNotExist:
                return Response(data={DETAIL: NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:  # Much customizations are made in this method, catch any unexpected errors
            from config.loggers import log_exception
            log_exception(e)
            return Response(data={DETAIL: BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
