# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

MY_APPS = [
    'logs',
]

INSTALLED_APPS = [
    'django_filters',
]

DEV_APS = [
    'debug_toolbar',
]

PROD_APS = [

]

INSTALLED_APPS = DJANGO_APPS + INSTALLED_APPS + MY_APPS

