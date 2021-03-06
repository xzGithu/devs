"""
Django settings for devs project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
# import django_redis
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# from django.core.cache import cache
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qpj0@fv)td8!f7@h0fh%g22swxt_l4j0!a2^tw5@6x2c350=d!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False
ALLOWED_HOSTS = ['*']

# Application definition
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
             # "PASSWORD": "yoursecret",
        },
    },
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'devsapp',
    'crispy_forms',
    'rest_framework',
    # 'easy_thumbnails',
    # 'filer',
    # 'mptt',
    # 'operation.apps.OperationConfig',

]

THUMBNAIL_HIGH_RESOLUTION=True
THUMBNAIL_PROCESSORS={
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'devs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'devs.wsgi.application'

# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES':[
#         'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
#     ]
# }
# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'TEST': {
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci'
        }
        # 'NAME':'ans',
        # 'HOST':'192.168.137.153',
        # 'PORT':3306,
        # 'USER':'root',
        # 'PASSWORD':'',

    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

# LANGUAGE_CODE = 'en-us'

LANGUAGE_CODE = 'zh-cn'
TIME_ZONE = 'UTC'
# ANGUAGE_CODE = 'zh-cn'
USE_I18N = True

USE_L10N = True

USE_TZ = True

CSRF_COOKIE_HTTPONLY = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
# AUTH_USER_MODEL='operation.ExtendUser'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static'),
)
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# LOGIN_URL = '/login/'
# LOGIN_URL='/course/mine/'
FILE_IGNORE_LIST=''
DOCUMENT_ROOT='/soft/doc'
# LOGIN_REDIRECT_URL='/course/mine/'
# FILE_UPLOAD_MAX_SIZE=10240
