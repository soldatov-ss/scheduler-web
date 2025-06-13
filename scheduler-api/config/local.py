import logging
import os
from .common import Common
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Local(Common):
    DEBUG = True

    # Testing
    INSTALLED_APPS = Common.INSTALLED_APPS
    MIDDLEWARE = Common.MIDDLEWARE

    # Mail
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    CORS_ORIGIN_ALLOW_ALL = True

    SILK_ENABLED = os.getenv("SILK_ENABLED", "no").lower() in ("true", "1", "yes")

    SILKY_PYTHON_PROFILER = True
    profilers_apps = ("nplusone.ext.django", "silk")
    profilers_middlewares = ("nplusone.ext.django.NPlusOneMiddleware", "silk.middleware.SilkyMiddleware")

    INSTALLED_APPS += profilers_apps
    MIDDLEWARE += profilers_middlewares

    NPLUSONE_LOGGER = logging.getLogger("nplusone")
    NPLUSONE_LOG_LEVEL = logging.INFO
