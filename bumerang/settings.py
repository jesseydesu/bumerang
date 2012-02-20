# -*- coding: utf-8 -*-
import os

from bumerang.local_settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
    #('Your Name', 'alexei.iljin@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'bumerang.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

TIME_ZONE = 'Europe/Moscow'

LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

MEDIA_URL = 'http://62.76.179.205/media/'

FILE_UPLOAD_TEMP_DIR = os.path.join(MEDIA_ROOT, 'tmp')
FILE_UPLOAD_PERMISSIONS = 777

if LOCALHOST:
    MEDIA_URL = 'http://localhost:8000/media/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

STATIC_URL = '/static/'

#ADMIN_MEDIA_PREFIX = '/static/admin/'
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates/static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'c=2wrnal@-sxi&8^^a*zp4x!k!q@nr(*p__dw4*==lgfvvp@_f'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',

    'bumerang.apps.accounts.context_processors.global_login_form',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'bumerang.apps.accounts.middleware.KeepLoggedInMiddleware',
)

if DEBUG:
    MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
        'bumerang.apps.utils.middleware.ProfilerMiddleware',)

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Keep me logged settings
KEEP_LOGGED_KEY = 'keep_me_logged'
KEEP_LOGGED_DURATION = 30  # in days


# used this component:
# https://github.com/martinrusev/django-redis-sessions
#SESSION_ENGINE = 'redis_sessions.session'
#SESSION_REDIS_HOST = '10.0.0.10'
#SESSION_REDIS_PORT = 6379
#SESSION_REDIS_DB = 0
#SESSION_REDIS_PASSWORD = 'fr6kdrWqDlRu8kktHv4FzhlH4CgW3JPC'

ROOT_URLCONF = 'bumerang.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

AUTH_PROFILE_MODULE = 'bumerang.apps.accounts.models.Profile'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'sitetree',
    'django.contrib.flatpages',
    'django.contrib.staticfiles',
    'grappelli',
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.admindocs',

    # internal
    'bumerang.apps.bumerang_site',
    'bumerang.apps.news',
    'bumerang.apps.advices',
    'bumerang.apps.video',
    'bumerang.apps.video.albums',
    'bumerang.apps.video.playlists',
    'bumerang.apps.video.converting',
    'bumerang.apps.photo',
    'bumerang.apps.photo.albums',
    'bumerang.apps.accounts',
    'bumerang.apps.utils',

    # external
    'south',
    'mptt',
    'tinymce',
    'djcelery',
    'djkombu',
)

TINYMCE_JS_URL = os.path.join(STATIC_ROOT, "tiny_mce/tiny_mce.js")
TINYMCE_JS_ROOT = os.path.join(MEDIA_ROOT, "tiny_mce")

TINYMCE_PLUGINS = [
    'safari',
    'table',
    'advlink',
    'advimage',
    'iespell',
    'inlinepopups',
    'media',
    'searchreplace',
    'contextmenu',
    'paste',
    'wordcount'
]
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,paste,searchreplace",
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    }

FILEBROWSER_DIRECTORY = 'uploads/'

GRAPPELLI_ADMIN_TITLE = u'Bumerang'

FIXTURE_DIRS = (
    os.path.join(PROJECT_ROOT, 'fixtures'),
)

PREVIEWS_COUNT = 5

if DEBUG:
#    INSTALLED_APPS += ('debug_toolbar',)
#    INSTALLED_APPS += ('django_extensions',)
#
#    DEBUG_TOOLBAR_PANELS = (
#        'debug_toolbar.panels.version.VersionDebugPanel',
#        'debug_toolbar.panels.timer.TimerDebugPanel',
#        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
#        'debug_toolbar.panels.headers.HeaderDebugPanel',
#        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
#        'debug_toolbar.panels.template.TemplateDebugPanel',
#        'debug_toolbar.panels.sql.SQLDebugPanel',
#        'debug_toolbar.panels.signals.SignalDebugPanel',
#        'debug_toolbar.panels.logger.LoggingPanel',
#    )
#
#    INTERNAL_IPS = ('127.0.0.1',)
#    DEBUG_TOOLBAR_CONFIG = dict(
#        INTERCEPT_REDIRECTS=False
#    )

    STATICFILES_DIRS += (os.path.join(PROJECT_ROOT, 'media'),)

EMAIL_NOREPLY_ADDR = 'noreply@bumerangpro.com'

import djcelery
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
BROKER_BACKEND = "djkombu.transport.DatabaseTransport"
BROKER_POOL_LIMIT = 10
djcelery.setup_loader()
