from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG


INSTALLED_APPS += (
    'debug_toolbar',
    'django_nose',
    'django_coverage',
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


LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'start'
LOGOUT_URL = 'logout'

AUTHENTICATION_BACKENDS = (
    'noncense.backends.PhoneBackend',
    'django.contrib.auth.backends.ModelBackend',)

AUTH_USER_MODEL = 'noncense.MobileUser'

TWILIO_ACCOUNT_SID = get_env_variable("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = get_env_variable("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = get_env_variable("TWILIO_FROM_NUMBER")
