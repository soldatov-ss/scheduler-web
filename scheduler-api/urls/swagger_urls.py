from django.conf import settings
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = (
    [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        # Swagger UI
        path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
        # Redoc UI
        path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    ]
    if settings.APP_ENV != "production"
    else []
)
