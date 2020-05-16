from .base import *

from decouple import Csv, Config, RepositoryEnv

# Set config as .env.dev file
env_path = 'notebook/settings/.env'
env_config = Config(RepositoryEnv(env_path))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env_config.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env_config.get('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = env_config.get('ALLOWED_HOSTS', cast=Csv())

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env_config.get('DB_NAME'),
        'USER': env_config.get('DB_USER'),
        'PASSWORD': env_config.get('DB_PASSWORD'),
        'HOST': env_config.get('DB_HOST'),
        'PORT': env_config.get('DB_PORT'),
    }
}

# Auth Settings

# Change when using custom domain.
LOGIN_URL = '/production/accounts/signin'
LOGIN_REDIRECT_URL = '/production/notes'
LOGOUT_REDIRECT_URL = '/production'

# Python social auth

SOCIAL_AUTH_GITHUB_KEY = env_config.get('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = env_config.get('SOCIAL_AUTH_GITHUB_SECRET')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env_config.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env_config.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

# Sentry 

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://ba59b807fba94d9680144eb6bc86e9f1@o318909.ingest.sentry.io/5242620",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)


# S3

AWS_ACCESS_KEY_ID = env_config.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env_config.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env_config.get('AWS_STORAGE_BUCKET_NAME')

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_REGION_NAME = 'eu-west-2'


AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=31536000',
}
AWS_LOCATION = 'static'

STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'