import os

import dj_database_url

from .base import *


DEBUG = True

ALLOWED_HOSTS = [
    ".herokuapp.com"
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    *MIDDLEWARE
]

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ["REDIS_URL"],
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ["CLOUDINARY_CLOUD_NAME"],
    'API_KEY': os.environ["CLOUDINARY_API_KEY"],
    'API_SECRET': os.environ["CLOUDINARY_API_SECRET"]
}

MEDIA_URL = "/media/"
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
