from .base import *


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# Uncomment 'USER' and 'PASSWORD' if you have username and password for your database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'travis_ci_test',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
