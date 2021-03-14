from django_filters import FilterSet

from apps.promos.models import Promo


class PromoFilter(FilterSet):
    class Meta:
        model = Promo
        exclude = ('description',)
