from django.contrib import admin

from apps.promos.models import Promo
from apps.users.constants import NORMAL_USER
from apps.users.models import CustomUser


class PromoAdmin(admin.ModelAdmin):
    pass

    # Show non admin users only in promo users
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context['adminform'].form.fields['user'].queryset = CustomUser.objects.filter(role=NORMAL_USER)
        return super(PromoAdmin, self).render_change_form(request, context, add, change, form_url, obj)


admin.site.register(Promo, PromoAdmin)
