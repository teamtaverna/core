from .base import *

DEBUG = True
ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# Uncomment 'USER' and 'PASSWORD' if you have username and password for your database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': dotenv.get('DB_NAME'),
        'USER': dotenv.get('DB_USER', ''),
        'PASSWORD': dotenv.get('DB_PASSWORD', ''),
        'HOST': '127.0.0.1',
        'PORT': dotenv.get('DB_PORT', '5432'),
    }
}
