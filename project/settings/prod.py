from .base import *

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

AWS_ACCESS_KEY_ID = get_env_variable("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env_variable("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = get_env_variable("AWS_STORAGE_BUCKET_NAME")


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

INSTALLED_APPS += (
    'storages',
    # 'raven.contrib.django.raven_compat',
)


# RAVEN_CONFIG = {
#     'dsn': 'https://1c947653a03f40fdaff079078a8b7f8f:f0499a280d924910959a850a165c3a67@app.getsentry.com/10264',
# }


STATIC_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

DEBUG = bool(get_env_variable("DJANGO_DEBUG"))
TEMPLATE_DEBUG = DEBUG
