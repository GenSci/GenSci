from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "+vi&bj@o^e9#)v#mrh8e)repzs)@!2cmgnp5_v656em)uhf-nl"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

INTERNAL_IPS = ["127.0.0.1", "172.18.0.3"]

# INSTALLED_APPS += [
#     'debug_toolbar'
# ]
# MIDDLEWARE = [
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# ] + MIDDLEWARE

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SHOW_TOOLBAR_CALLBACK = "gensci.settings.dev.show_toolbar"


def show_toolbar():
    return True


try:
    from .local import *
except ImportError:
    pass
