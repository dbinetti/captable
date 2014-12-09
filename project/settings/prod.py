from .base import *

DEBUG = True
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
    'raven.contrib.django.raven_compat',
)

MEDIA_ROOT = "/{0}/".format(DEFAULT_S3_PATH)
STATIC_ROOT = "/{0}/".format(STATIC_S3_PATH)

STATIC_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/static/'
MEDIA_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/media/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

ALLOWED_HOSTS = [get_env_variable("HEROKU_HOST")]

RAVEN_CONFIG = {
    'dsn': 'https://a16d1dadc8b34ed0ac7d70e5abbdc931:f807666c30b641e8b8a8084b96c8062a@app.getsentry.com/11747',
}

