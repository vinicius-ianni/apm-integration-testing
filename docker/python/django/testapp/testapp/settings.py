"""
Django settings for testapp project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^w%5$)6etp(n(t+vgeiqosoc*w)+^#u&)727bg)ik-vmtr%wn6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'elasticapm.contrib.django',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

ELASTIC_APM = {
    'SERVICE_NAME': os.environ['DJANGO_SERVICE_NAME'],
    'SERVER_URL': os.environ['APM_SERVER_URL'],
    'SERVER_URL': os.environ['APM_SERVER_URL'],
    'SECRET_TOKEN': '1234_test',
    'TRANSACTION_SEND_FREQ': 1,
    'MAX_EVENT_QUEUE_LENGTH': 1,
    'TRANSACTIONS_IGNORE_PATTERNS': ['.*healthcheck']
}

MIDDLEWARE = [
    'elasticapm.contrib.django.middleware.TracingMiddleware',
    'elasticapm.contrib.django.middleware.Catch404Middleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'testapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(process)d %(message)s'
        },
    },
    'handlers': {
        'elasticapm': {
            'level': 'WARNING',
            'class': 'elasticapm.contrib.django.handlers.LoggingHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'mysite': {
            'level': 'WARNING',
            'handlers': ['elasticapm'],
            'propagate': False,
        },
        # Log errors from the Elastic APM module to the console (recommended)
        'elasticapm.errors': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
