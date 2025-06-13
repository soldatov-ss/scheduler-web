"""Development urls module."""

from django.conf import settings
from django.urls import include, path

urlpatterns = []

# This is only needed when using runserver.
if settings.DEBUG:
    if settings.SILK_ENABLED:
        try:
            import silk  # noqa

            urlpatterns.append(path("silk/", include("silk.urls", namespace="silk")))
        except (ImportError, RuntimeError):
            pass
