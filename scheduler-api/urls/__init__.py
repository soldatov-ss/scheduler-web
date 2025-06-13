from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path, reverse_lazy
from django.views.generic.base import RedirectView
from .swagger_urls import urlpatterns as swagger_patterns
from .development_urls import urlpatterns as development_urlpatterns
# API v1 app URLs
api_v1_apps_urls = [
    path("", include("scheduler-api.apps.users.urls")),
]


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r"^$", RedirectView.as_view(url=reverse_lazy("api-root"), permanent=False)),
    path(
        "api/",
        include(
            [
                path(
                    "v1/",
                    include(api_v1_apps_urls),
                )
            ]
        ),
    ),
    path("", include(swagger_patterns)),
    path("", include(development_urlpatterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
