from .base import *


DEBUG = False

ALLOWED_HOSTS = ['*']

# Database
DATABASES = {
    'default': {
        'ENGINE': config("DATABASE_ENGINE"),
        'NAME': config("DATABASE_NAME"),
        'USER' : config("DATABASE_USER"),
        'PASSWORD': config("DATABASE_PASSWORD"),
        'HOST' : config("DATABASE_HOST"),
        'PORT' : config("DATABASE_PORT")
    }
}

# Cahce
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}