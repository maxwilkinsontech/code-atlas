from .base import *

from decouple import Csv, Config, RepositoryEnv

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#n0#j&y-j+$pjt5-iw&le8j@loxp)q%k)*7*d1@ctk@1!)fdaq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.localhost', '127.0.0.1', '192.168.0.61']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django_notebook_dev',
        'USER': 'django_notebook',
        'PASSWORD': 'superuser',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# Email Settings

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Set config as .env.dev file
# Using try expecpt so that tests can be run via GitHub Actions.
try:
    env_path = 'notebook/settings/.env.local'
    env_config = Config(RepositoryEnv(env_path))
except:
    env_config = {}

# Python Social Auth

SOCIAL_AUTH_GITHUB_KEY = env_config.get('SOCIAL_AUTH_GITHUB_KEY', '')
SOCIAL_AUTH_GITHUB_SECRET = env_config.get('SOCIAL_AUTH_GITHUB_SECRET', '')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env_config.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY', '')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env_config.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET', '')