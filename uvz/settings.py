"""
Django settings for uvz project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-dcrxggckdn%w()3*afs=dr7b)hl8x0t%-fxzhdta3w^y-h1bf^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "False")

ALLOWED_HOSTS = [
    "uvz.herokuapp.com",
    "127.0.0.1"
]

# Set CRFR cokie secure, so can be posted from postman
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# Application definition

INSTALLED_APPS = [
    'uvz',
    'background_task',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'uvz.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates/"],
        'APP_DIRS': False,
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

WSGI_APPLICATION = 'uvz.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

import dj_database_url
DATABASES = {
    'default': dj_database_url.parse(os.environ["DATABASE_URL"])
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = ["static/"]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Custom settings

# API KEYS
# GMAIL API config
GMAIL_API_CONFIG = {
    "web": {
        "client_id": "29973129776-30to7tprmv25vlec7riikl75nlh3c9d1.apps.googleusercontent.com",
        "project_id": "rss-uvz",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "FJNESCPmPfHjvFMs7VyHHmOh",
        "redirect_uris": [
            "https://rss-uvz.firebaseapp.com/__/auth/handler"
        ],
        "javascript_origins": [
            "http://localhost",
            "http://localhost:5000",
            "https://rss-uvz.firebaseapp.com"
        ]
    }
}
# Enable httpOnly cookies
SESSION_COOKIE_PATH = '/;HttpOnly'
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
# Url to redirect to
LOGIN_URL = "/"
# Settings module path
DJANGO_SETTINGS_MODULE = "uvz"
