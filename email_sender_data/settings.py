import os
from distutils.util import strtobool
from pathlib import Path

import dj_database_url
import environ
from datetime import timedelta

# from sendgrid_backend import SendgridBackend


env = environ.Env()
environ.Env.read_env()

# Base directory of the Django project
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key for cryptographic signing
SECRET_KEY = env("SECRET_KEY")

# Debug mode (True or False)
DEBUG = strtobool(env("DEBUG"))

# List of allowed host addresses
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# Host address of the applications
HOST_ADDRESS = env("HOST_ADDRESS")

# List of origins that are trusted for CSRF protections
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

# Email settings
EMAIL_HOST = "smtp.sendgrid.net"  # SMTP server for sending emails
EMAIL_HOST_USER = "apikey"  # Email host username retrieved from environment variables
# Email host password retrieved from environment variables
EMAIL_HOST_PASSWORD = env("SENDGRID_API_KEY")
EMAIL_PORT = 587  # Port for the SMTP server
EMAIL_USE_TLS = True  # Enable TLS encryption for secure email communication
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"  # Email backend for sending emails
DEFAULT_FROM_EMAIL = "info@trounceflow.com"  # Default sender email address

# AWS settings
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_STORAGE_FOLDER = env("AWS_STORAGE_FOLDER")
AWS_QUERYSTRING_AUTH = False

# EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = env("SENDGRID_API_KEY")

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # Change it to False to allow specific origins

# Maximum size for file uploads (100 megabytes)
DATA_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024  # 100 gegabytes

# List of installed Django applications
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "email_sender",
    "funds",
    "exante_data",
    "rangefilter",
    "data_importer",
    "django_admin_listfilter_dropdown",
    "djoser",
    "accounts",
]

# Middleware classes
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Security middleware
    "django.contrib.sessions.middleware.SessionMiddleware",  # Session middleware
    "django.middleware.common.CommonMiddleware",  # Common middleware
    "django.middleware.csrf.CsrfViewMiddleware",  # CSRF middleware
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Authentication middleware
    "django.contrib.messages.middleware.MessageMiddleware",  # Message middleware
    # X-Frame-Options middleware
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # CORS middleware
    "django.middleware.security.SecurityMiddleware",  # Additional security middleware
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Whitenoise middleware
]

# Root URL configuration module
ROOT_URLCONF = "exante_data.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI application module
WSGI_APPLICATION = "exante_data.wsgi.application"

# Database settings
DATABASES = {
    "default": dj_database_url.config(default=env("DEFAULT_DATABASE_URL")),
    "funds_db": dj_database_url.config(default=env("FUNDS_DATABASE_URL")),
}
DATABASE_ROUTERS = ["exante_data.router.DbRouter"]


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "exante_data", "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "static")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

DJOSER = {
    "LOGIN_FIELD": "email",
    "USER_CREATE_PASSWORD_RETYPE": True,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "SET_USERNAME_RETYPE": True,
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL": "email/reset/confirm/{uid}/{token}",
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": True,
    "DOMAIN": env("FRONTEND_DOMAIN"),
    "SERIALIZERS": {
        "user_create": "accounts.serializers.UserCreateSerializer",
        "user": "accounts.serializers.UserCreateSerializer",
        "user_delete": "djoser.serializers.UserDeleteSerializer",
    },
    "EMAIL": {
        "activation": "accounts.email.ActivationEmail",
        "confirmation": "accounts.email.ConfirmationEmail",
        "password_reset": "accounts.email.PasswordResetEmail",
        "password_changed_confirmation": "accounts.email.PasswordChangedConfirmationEmail",
        "username_changed_confirmation": "accounts.email.UsernameChangedConfirmationEmail",
        "username_reset_confirmation": "accounts.email.UsernameResetConfirmationEmail",
    },
}


AUTH_USER_MODEL = "accounts.UserAccount"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}
