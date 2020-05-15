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