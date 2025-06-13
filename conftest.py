import os
from configurations import setup
import pytest


# 1. Set env vars first
# This is needed for django-configurations
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scheduler-api.config")
os.environ.setdefault("DJANGO_CONFIGURATION", "Local")

# 2. Setup django-configurations BEFORE importing anything Django-related
setup()

# 3. Safe to import Django modules now

# Ensures pytest waits for the database to load
# https://pytest-django.readthedocs.io/en/latest/faq.html#how-can-i-give-database-access-to-all-my-tests-without-the-django-db-marker
@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass

