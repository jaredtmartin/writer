# Django settings for webservices project.
import os, sys

DIRNAME = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.path.dirname(__file__)) + os.sep
DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_DOMAIN = "writeraxis-python.appspot.com"

from pprint import pprint as pp
# print "BASE_DIR = %s" % str(BASE_DIR) 
extra_modules="%senv/lib/python2.7/site-packages/" % BASE_DIR
# print "extra_modules = %s" % str(extra_modules)

# print "+++++++++++++++++++++++++++++++++++ Before +++++++++++++++++++++++++++++++++++++++"
# pp(sys.path)
# print "+++++++++++++++++++++++++++++++++++ After  +++++++++++++++++++++++++++++++++++++++"
sys.path+=[extra_modules]
# pp(sys.path)


ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'webservices',                      # Or path to database file if using sqlite3.
#         'USER': 'root',                      # Not used with sqlite3.
#         'PASSWORD': 't1bur0n',                  # Not used with sqlite3.
#         'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#         'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#     }
# }


if (os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine') or
    os.getenv('SETTINGS_MODE') == 'prod'):
    # Running on production App Engine, so use a Google Cloud SQL database.
    DATABASES = {
        'default': {
            'ENGINE': 'google.appengine.ext.django.backends.rdbms',
            'INSTANCE': 'writeraxis-python:writeraxis',
            'NAME': 'writeraxis',
        }
    }
else:
    # Running in development, so use a local MySQL database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'USER': 'root',
            'PASSWORD': 't1bur0n',
            'HOST': 'localhost',
            'NAME': 'writeraxis',
        }
    }


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = "587"
EMAIL_HOST_USER = 'writeraxis@gmail.com'
EMAIL_HOST_PASSWORD = '179862934'
EMAIL_USE_TLS = True
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: "/users/%s/%s/" % (u.username,u.pk),
}
EMAIL_FROM = ""

AUTH_PROFILE_MODULE = 'articles.UserProfile' # Forms relys on this to be set to the following: forms.UserProfile

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(DIRNAME, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"

STATIC_ROOT = os.path.join(DIRNAME, 'static/')
CKEDITOR_UPLOAD_PATH = os.path.join(STATIC_ROOT, 'ckeditor_uploads/')
# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

TEMPLATE_CONTEXT_PROCESSORS = (
#    'django_facebook.context_processors.facebook',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'articles.context_processors.login_form',
)

AUTHENTICATION_BACKENDS = (
    #'django_facebook.auth_backends.FacebookBackend',
    # 'auth.FacebookProfileBackend',
#    'django_facebook.auth.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # os.path.join(DIRNAME, 'project_static/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'w_vg+d$laknf#k*v=sph2y_tr0-1875k(xe26y@(8q-)q!b=1x'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
   'debug_toolbar.middleware.DebugToolbarMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django_facebook.middleware.FacebookMiddleware',
    # 'middleware.FacebookMiddleware',
    'middleware.TimezoneMiddleware',
    
)
INTERNAL_IPS = ('127.0.0.1','localhost')
ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
#WSGI_APPLICATION = 'webservices.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # os.path.join(DIRNAME, 'feedback/templates/'),
    # os.path.join(DIRNAME, 'templates/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'django.contrib.markup',
    # 'knowledge',
    'django_extensions',
    'accounts',
    # 'django_facebook',
    #'forms',
    'articles',
    'slick',
    'design',
    # 'common',
    #'django_actions',

)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
#LOGIN_URL='https://www.facebook.com/dialog/oauth?client_id=YOUR_APP_ID&redirect_uri=YOUR_REDIRECT_URI&state=SOME_ARBITRARY_BUT_UNIQUE_STRING'
LOGIN_URL='/accounts/login/'
LOGIN_REDIRECT_URL = "/articles/dashboard/"
################### Facebook Integration Settings ################### 
FACEBOOK_APP_ID = '519129288106424'
FACEBOOK_APP_SECRET = '93c96e8759a2a91bd13336d32e398795'
FACEBOOK_SECRET_KEY = '93c96e8759a2a91bd13336d32e398795'
#AUTH_PROFILE_MODULE = 'django_facebook.FacebookProfile'
PROFILE_IMAGE_PATH = os.path.join(MEDIA_URL, 'facebook_profiles/%Y/%m/%d')
FACEBOOK_CANVAS_PAGE = 'https://apps.facebook.com/%s/' % FACEBOOK_APP_ID
FACEBOOK_SCOPE = ['manage_pages']

# If manage.py test was called, use SQLite
import sys
# if 'test' in sys.argv:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ('test_sqlite.db')
    }
}
#     DEBUG = True
# else:
INSTALLED_APPS=INSTALLED_APPS+('debug_toolbar',)

OAUTH_SECRET="tddEThmU8NgXnXz9cnKMjrLAZzdmC5EhhnLinHNwEdEpE"
OAUTH_TOKEN='fW9kmLKH8qvCrAY6Amt5p3qBJwh1LMnseeG56fGd'
CONSUMER_SECRET="DlzUgtRvbMFSTP1wFLY4YuOZtZus59EreDoP8kdSpw"
CONSUMER_KEY="weGHEJZMZs0h9bnpLouBSw"


