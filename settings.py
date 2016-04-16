# coding=utf-8
from __future__ import absolute_import, unicode_literals
from __future__ import print_function

import os

SECRET_KEY = u'secret_key'

ALLOWED_HOSTS = ['*']
TIME_ZONE = u'UTC'
USE_TZ = True
LANGUAGE_CODE = u'en'
LANGUAGES = (
    (u'en', u'English'),
)
DEBUG = True
INTERNAL_IPS = (u'127.0.0.1', u'192.168.99.100')
# AUTH_USER_MODEL = u'core.User'
ANONYMOUS_USER_ID = -1

CACHES = {
    u'default': {
        u'BACKEND': u'django.core.cache.backends.dummy.DummyCache',
    }
}

DEFAULT_TABLESPACE = u'tables'

DATABASES = {
    u'default': {
        u'ENGINE': u'django.db.backends.sqlite3',
    }
}

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIRNAME = PROJECT_ROOT.split(os.sep)[-1]
ROOT_URLCONF = u'%s.urls' % PROJECT_DIRNAME

USE_SOUTH = False

INSTALLED_APPS = (
    u'django.contrib.admin',
    u'django.contrib.auth',
    u'django.contrib.contenttypes',
    u'django_neo4j',
    u'django_neo4j.tests',
    u'django_nose',
)

PROJECT_APPS = (
    u'django_neo4j',
)

TEST_RUNNER = u'django_nose.NoseTestSuiteRunner'

MIDDLEWARE_CLASSES = (
    u'django.contrib.sessions.middleware.SessionMiddleware',
    u'django.contrib.auth.middleware.AuthenticationMiddleware',
    u'django.middleware.security.SecurityMiddleware',
)

REST_FRAMEWORK = {
    u'TEST_REQUEST_DEFAULT_FORMAT': u'json',
    u'TEST_REQUEST_RENDERER_CLASSES': (
        u'rest_framework.renderers.JSONRenderer',
    ),
}

NOSE_ARGS = [
    u'--with-coverage',
    u'--cover-html',
    u'--cover-html-dir=coverage',
    u'--cover-package=django_neo4j',
    u'--nocapture',
]
