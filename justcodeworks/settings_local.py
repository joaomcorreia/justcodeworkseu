"""
Local development settings for JustCodeWorks.EU
Uses SQLite for simplicity and includes tenant configuration
"""

from .settings import *
import os

# Override database for local development with PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'justcodeworks_local',
        'USER': 'postgres',
        'PASSWORD': 'password',  # Change this to your local PostgreSQL password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# For local development, we'll use a simplified setup
# Keep all the tenant settings from the main settings.py
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.localhost']

# Simplified logging for development
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
    },
}

print("🚀 Using LOCAL DEVELOPMENT settings with simplified database")