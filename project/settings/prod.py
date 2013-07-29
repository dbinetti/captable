from .base import *

DEBUG = bool(get_env_variable("DJANGO_DEBUG"))
TEMPLATE_DEBUG = DEBUG

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

AWS_ACCESS_KEY_ID = get_env_variable("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env_variable("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = get_env_variable("AWS_STORAGE_BUCKET_NAME")


DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'

DEFAULT_S3_PATH = "media"
STATIC_S3_PATH = "static"


INSTALLED_APPS += (
    'storages',
    's3_folder_storage',
    # 'raven.contrib.django.raven_compat',
)

MEDIA_ROOT = "/{0}/".format(DEFAULT_S3_PATH)
STATIC_ROOT = "/{0}/".format(STATIC_S3_PATH)

STATIC_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/static/'
MEDIA_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/media/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

ALLOWED_HOSTS = [get_env_variable("HEROKU_HOST")]

# RAVEN_CONFIG = {
#     'dsn': 'https://1c947653a03f40fdaff079078a8b7f8f:f0499a280d924910959a850a165c3a67@app.getsentry.com/10264',
# }

