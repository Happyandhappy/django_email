"""
Django settings for vhodove project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ADMINS = (
    ('Cvetozar Ninov', 'cninov@gmail.com'),
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@w72%u2yh&v$h2(%x485fvj)^e$#8khz0*@l(kqt!^6v3=)tg8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', 'system.vhodove.bg']

INTERNAL_IPS = ['127.0.0.1',]

DATE_FORMAT = 'd.m.Y'
DATE_INPUT_FORMATS = ('%d.%m.%Y', '%Y-%m-%d')
FIRST_DAY_OF_WEEK = 1

#SESSION_EXPIRE_AT_BROWSER_CLOSE = False
#SESSION_COOKIE_AGE = 60 * 60
#SESSION_SAVE_EVERY_REQUEST = True

# Application definition

INSTALLED_APPS = (
    'django_admin_bootstrapped.bootstrap3',
    'django_admin_bootstrapped',
    'bootstrap_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'smart_selects',
    'documents',
    'nomenclatures',
    'tasks',
    'entrances',
    'dynamic_costs',
    'colorful',
    'ckeditor',
    'rosetta',
    'select2',
    'client_emails',
    'debug_toolbar',
    'django_user_agents',
    # 'rangefilter',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
)

ROOT_URLCONF = 'vhodove.urls'

WSGI_APPLICATION = 'vhodove.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

from django.utils.translation import ugettext_lazy as _

LANGUAGES = (
    ('bg', _('Bulgarian')),
)

LANGUAGE_CODE = 'bg'

TIME_ZONE = 'Europe/Sofia'

USE_I18N = True

USE_L10N = False

USE_TZ = True

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    'django.core.context_processors.request',
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "vhodove.context_processors.attach_entrance",
    )


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = 'http://static.vhodove.bg/media/'

CKEDITOR_UPLOAD_PATH = os.path.join(BASE_DIR, 'media/ckeditor/')

STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)


CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'height': 300,
        'width': '100%',
        'toolbar_Full': [
        ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'Undo', 'Redo'],
        ['Image', 'Table', 'HorizontalRule'], ['NumberedList', 'BulletedList'],
        ['TextColor', 'BGColor'],
    ],
    },
}
