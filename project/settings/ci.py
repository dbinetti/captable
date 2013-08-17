from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG


INSTALLED_APPS += (
    'django_nose',
    'django_coverage',
)


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

INTERNAL_IPS = ('127.0.0.1',)


MEDIA_ROOT = PROJECT_ROOT.ancestor(2).child("localstorage").child(PROJECT_NAME).child("media")
MEDIA_URL = '/media/'

STATIC_ROOT = PROJECT_ROOT.ancestor(2).child("localstorage").child(PROJECT_NAME).child("static")
STATIC_URL = '/static/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
