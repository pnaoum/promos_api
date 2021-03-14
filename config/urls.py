from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.users.views import Login, SignUp
from config import settings
from config.settings import DEBUG

API_V1_PREFIX = 'api/v1/'
auth_urlpatterns = [
    path(API_V1_PREFIX + 'auth/login/', Login.as_view()),
    path(API_V1_PREFIX + 'auth/signup/', SignUp.as_view()),
]

apps_urlpatterns = [
    path(API_V1_PREFIX, include(('apps.core.urls', 'core'))),
    path(API_V1_PREFIX, include(('apps.promos.urls', 'promos'))),
]
urlpatterns = auth_urlpatterns + apps_urlpatterns
urlpatterns += [path(API_V1_PREFIX, include('swagger.urls'))] + static(settings.STATIC_URL,
                                                                       document_root=settings.STATIC_ROOT)

# Show admin in development mode only
if DEBUG:
    urlpatterns += [
        path('admin/', admin.site.urls),
    ]
