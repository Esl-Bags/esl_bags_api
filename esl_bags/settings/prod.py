from esl_bags.settings.base import *

ALLOWED_HOSTS = ['esl-bags.caprover-dev.claudinosa.com.br']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": config('USER'),
        "PASSWORD": config('PASSWORD'),
        "HOST": config('HOST'),
        "PORT": config('PORT'),
    }
}

#Email backend configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = config('MAIL_USER')
EMAIL_HOST_PASSWORD = config('MAIL_PASSWORD')