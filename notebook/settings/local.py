from .base import *

from decouple import Csv, Config, RepositoryEnv

# Set config as .env.dev file
env_path = 'notebook/settings/.env.local'
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


# Python Social Auth

SOCIAL_AUTH_GITHUB_KEY = env_config.get('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = env_config.get('SOCIAL_AUTH_GITHUB_SECRET')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env_config.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env_config.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')