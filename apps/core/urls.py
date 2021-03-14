from django.urls import path

from apps.core.views import HealthCheck

urlpatterns = [
    path('health', HealthCheck.as_view())
]
