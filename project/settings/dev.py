from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG


INSTALLED_APPS += (
    'debug_toolbar',
    'django_nose',
    'django_coverage',
    'django_extensions',
)

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

MEDIA_ROOT = PROJECT_ROOT.ancestor(2).child("localstorage").child(PROJECT_NAME).child("media")
MEDIA_URL = '/media/'

STATIC_ROOT = PROJECT_ROOT.ancestor(2).child("localstorage").child(PROJECT_NAME).child("static")
STATIC_URL = '/static/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
