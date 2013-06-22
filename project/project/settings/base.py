# Django settings for project project.
import os

from unipath import Path

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    """Get the environment variable or return exception"""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {var_name} environment variable".format(var_name=var_name)
        raise ImproperlyConfigured(error_msg)


PROJECT_ROOT = Path(__file__).ancestor(3)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
)

MANAGERS = ADMINS

ALLOWED_HOSTS = []

TIME_ZONE = 'America/Los_Angeles'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = PROJECT_ROOT.child("media")

MEDIA_URL = ''

STATIC_ROOT = PROJECT_ROOT.child("static")

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    PROJECT_ROOT.child("assets"),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = get_env_variable("SECRET_KEY")

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'

TEMPLATE_DIRS = (
    PROJECT_ROOT.child("templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'django.contrib.formtools',
    'south',
    'django_tables2',
    'captable',
    'noncense',
)
