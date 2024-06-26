"""
Django settings for Litomici_memeber_system project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from inspect import trace
import json
from operator import truediv
import dj_database_url
from pathlib import Path
from django.core.mail.backends.console import EmailBackend

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-wx6^cl3o#*h(cv7ax2f$rt53fasb=jq#6tk@7!5%_pom!&poft'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1800
ALLOWED_HOSTS = ['*']

#SMTP config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  # Use 587 for TLS or 465 for SSL
EMAIL_USE_TLS = True  # Use TLS for secure connection
#EMAIL_USE_SSL = False  # Use SSL for secure connection (if port is set to 465)
EMAIL_HOST_USER = 'turistaklitomici@gmail.com'
EMAIL_HOST_PASSWORD = 'cpep iyrd jgfe pzmz'
DEFAULT_FROM_EMAIL = 'your_email@gmail.com'
  # Use the generated app password if you set one
# DEFAULT_FROM_EMAIL = 'turistaklitomici@gmail.com'
# SERVER_EMAIL = 'turistaklitomici@gmail.com'

# Application definition

INSTALLED_APPS = [
    'Accounts',
    'Events',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions'
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'Litomici_memeber_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/"templates"],
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

WSGI_APPLICATION = 'Litomici_memeber_system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'NAME': BASE_DIR / 'db.sqlite3',
    }
}
DATABASES['default']=dj_database_url.parse('postgres://litomcampdb_user:eD7SrYIWnZTxn8J4devU7UxbaFeBQrrS@dpg-cngrag8l6cac73ag7qv0-a.frankfurt-postgres.render.com/litomcampdb') # type: ignore
GRAPH_MODELS ={
'all_applications': True,
'graph_models': True,
} 

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

##tady je problém s držením db 
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#             'CONNECTION_POOL_KWARGS': {'max_connections': 100},
#         }
#     }
# }


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/' 
STATIC_ROOT = BASE_DIR / 'staticFiles'
LOGOUT_REDIRECT_URL = "/login"
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
