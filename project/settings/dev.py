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

ADMINS = (
    (get_env_variable("FULL_NAME"), get_env_variable("USER_EMAIL")),
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

# STATIC_ROOT = '/Users/dbinetti/Repos/static'

STATIC_URL = '/static/'
