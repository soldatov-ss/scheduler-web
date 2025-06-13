import os

from .common import Common

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Test(Common):
    DEBUG = True
    CORS_ORIGIN_ALLOW_ALL = True

    # Testing
    INSTALLED_APPS = Common.INSTALLED_APPS
    MIDDLEWARE = Common.MIDDLEWARE

    # EMAIL
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
    EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025

    # https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
    TEST_RUNNER = "django.test.runner.DiscoverRunner"

    # CACHES
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#caches
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "",
        }
    }

    # PASSWORDS
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

    # TEMPLATES
    # ------------------------------------------------------------------------------
    Common.TEMPLATES[-1]["APP_DIRS"] = False
    Common.TEMPLATES[-1]["OPTIONS"]["loaders"] = [  # type: ignore[index] # noqa F405
        (
            "django.template.loaders.cached.Loader",
            [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        )
    ]

    # Disable logging during tests to reduce console noise
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": True,
        "handlers": {"null": {"class": "logging.NullHandler"}},
        "loggers": {"": {"handlers": ["null"], "level": "WARNING"}},
    }

    # Disable throttling
    Common.REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = []
