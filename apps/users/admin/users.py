from django.contrib import admin

from apps.users.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    fields = ('username', 'email', 'is_active', 'is_staff', 'is_superuser', 'address', 'role', 'mobile_number')


# admin.site.register(CustomUser, CustomUserAdmin)
