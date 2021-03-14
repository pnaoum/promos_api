from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.admin import admin as rest_admin
from rest_framework.authtoken.models import TokenProxy

admin.site.site_header = 'Promos API - Admin'
admin.site.site_title = 'Promos'
rest_admin.site.unregister(TokenProxy)
admin.site.unregister(Group)
