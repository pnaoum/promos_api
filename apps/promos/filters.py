from django_filters import FilterSet

from apps.promos.models import Promo


class PromoFilter(FilterSet):
    """
    Model Filter set for promo
    """

    class Meta:
        model = Promo
        exclude = ('description',)  # description is a text field, so it is excluded
