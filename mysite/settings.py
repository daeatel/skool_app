# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket
import mongoengine
from skool.settings import *

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# openshift is our PAAS for now.
ON_PAAS = 'OPENSHIFT_REPO_DIR' in os.environ

if ON_PAAS:
    SECRET_KEY = os.environ['OPENSHIFT_SECRET_TOKEN']
else:
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = ')_7av^!cy(wfx=k#3*7x+(=j^fzv+ot^1@sh9s9t=8$bu@r(z$'

# SECURITY WARNING: don't run with debug turned on in production!
# adjust to turn off when on Openshift, but allow an environment variable to override on PAAS
DEBUG = not ON_PAAS
DEBUG = DEBUG or 'DEBUG' in os.environ
DEBUG = True
if ON_PAAS and DEBUG:
    print("*** Warning - Debug mode is on ***")

TEMPLATE_DEBUG = True

if ON_PAAS:
    ALLOWED_HOSTS = [os.environ['OPENSHIFT_APP_DNS'], socket.gethostname()]
else:
    ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mysite',
    'debug_toolbar',
    'bootstrap_pagination',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# if ON_PAAS:
if False:
    # determine if we are on MySQL or POSTGRESQL
    if "OPENSHIFT_POSTGRESQL_DB_USERNAME" in os.environ:

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME':     os.environ['OPENSHIFT_APP_NAME'],
                'USER':     os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'],
                'PASSWORD': os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD'],
                'HOST':     os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],
                'PORT':     os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'],
            }
        }

    elif "OPENSHIFT_MYSQL_DB_USERNAME" in os.environ:

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME':     os.environ['OPENSHIFT_APP_NAME'],
                'USER':     os.environ['OPENSHIFT_MYSQL_DB_USERNAME'],
                'PASSWORD': os.environ['OPENSHIFT_MYSQL_DB_PASSWORD'],
                'HOST':     os.environ['OPENSHIFT_MYSQL_DB_HOST'],
                'PORT':     os.environ['OPENSHIFT_MYSQL_DB_PORT'],
            }
        }


else:
    # stock django, local development.
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #     }
    # }
    DATABASES = {
        'default': {
            'ENGINE': '',
        }
    }

SESSION_ENGINE = 'mongoengine.django.sessions'

_MONGODB_USER = MONGODB_USER
_MONGODB_PASSWD = MONGODB_USER
_MONGODB_HOST = MONGODB_HOST
_MONGODB_NAME = MONGODB_DB
_MONGODB_PORT = MONGODB_PORT
_MONGODB_DATABASE_HOST = 'mongodb://%s/%s' % (_MONGODB_HOST, _MONGODB_NAME)

if ON_PAAS:
    mongoengine.connect('skool', host=os.environ['OPENSHIFT_MONGODB_DB_HOST'], port=int(os.environ['OPENSHIFT_MONGODB_DB_PORT']), username="oshift", password="testing1234")
else:
    mongoengine.connect(_MONGODB_NAME, host=_MONGODB_DATABASE_HOST, port=_MONGODB_PORT)

AUTHENTICATION_BACKENDS = ('mongoengine.django.auth.MongoEngineBackend')


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'wsgi', 'static')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, "static"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)
