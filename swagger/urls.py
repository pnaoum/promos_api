from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from config.urls import urlpatterns
from .constants import SWAGGER_BASE_URL

schema_view = get_schema_view(
    openapi.Info(
        title="Promos API",
        default_version='v1',
        description="Promos API Documentation",
        contact=openapi.Contact(email="peter-naoum@hotmail.com"),
    ),
    permission_classes=(permissions.AllowAny,),
    public=True,
    patterns=urlpatterns
)

urlpatterns = [
    path(SWAGGER_BASE_URL, schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
