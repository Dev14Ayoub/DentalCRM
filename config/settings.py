import os
import sys
from pathlib import Path
from datetime import timedelta
import dj_database_url
from dotenv import load_dotenv
from django.contrib.messages import constants

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'INSECURE')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', '1') == '1'

LOCAL_RUN = False
if 'test' in sys.argv:
    LOCAL_RUN = True

ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS', 'localhost,127.0.0.1'
).strip().split(',')

CSRF_TRUSTED_ORIGINS = os.environ.get(
    'CSRF_TRUSTED_ORIGINS', 'https://localhost'
).strip().split(',')

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.app'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PHONENUMBER_DEFAULT_REGION = 'US'  # Set your country code
PHONENUMBER_DB_FORMAT = 'NATIONAL' 
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'drf_yasg',
    'base',
    'schedule',
    'users',
    'phonenumber_field',
    'dental.apps.DentalConfig',
    'rest_framework',
    'django_filters',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ]
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

if DEBUG and LOCAL_RUN:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]
    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ] + MIDDLEWARE
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: False,
    }

INTERNAL_IPS = [
    'localhost', '127.0.0.1',
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'base_static',
]

STATIC_ROOT = BASE_DIR / 'static'

# CORS settings
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS', 'https://localhost'
).strip().split(',')

# Database configuration
load_dotenv()

if DEBUG and LOCAL_RUN:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    db_config = dj_database_url.config(conn_max_age=600, ssl_require=True)
    if not db_config:
        db_config = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    DATABASES = {
        'default': db_config
    }

# Email configuration
EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')

EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'your_email@gmail.com')

EMAIL_HOST_PASSWORD = os.environ.get(
    'EMAIL_HOST_PASSWORD', 'your_email_password')

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)

EMAIL_LOGO_URL = os.environ.get('EMAIL_LOGO_URL', '')

# Internationalization
from django.utils.translation import gettext_lazy as _

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Etc/UTC'

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Removed LANGUAGES list to support all languages
# LANGUAGES = [
#     ('en', _('English')),
#     ('fr', _('Français (France)')),
# ]

# Message tags
MESSAGE_TAGS = {
    constants.DEBUG: 'message-debug',
    constants.ERROR: 'message-error',
    constants.SUCCESS: 'message-success',
    constants.INFO: 'message-info',
    constants.WARNING: 'message-warning',
}

# REST framework settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',  # noqa
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'PAGE_SIZE': 10,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "BLACKLIST_AFTER_ROTATION": False,
    "SIGNING_KEY": os.environ.get('SECRET_KEY_JWT', 'INSECURE'),
    "AUTH_HEADER_TYPES": ('Bearer',),
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'base_templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
