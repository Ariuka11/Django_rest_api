from .common import *

DEBUG = True

SECRET_KEY = "django-insecure-d)3c2_3@i+lsmdxpa5zpx+k!a*9=m%oma#)=@onfkz#vlnn2^n"

if DEBUG:
    MIDDLEWARE += ["silk.middleware.SilkyMiddleware"]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "store",
        "HOST": "localhost",
        "USER": "root",
        "PASSWORD": "jc1835",
    }
}
