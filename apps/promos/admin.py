from django.contrib import admin

from apps.promos.models import Promo


class PromoAdmin(admin.ModelAdmin):
    pass


admin.site.register(Promo, PromoAdmin)
