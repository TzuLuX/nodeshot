# Django settings for nodeshot project.

import os
import sys

sys.path.append('/var/www/nodeshot/')

DEBUG = True
SERVE_STATIC = DEBUG
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'nodeshot',                      # Or path to database file if using sqlite3.
        'USER': 'nodeshot',                      # Not used with sqlite3.
        'PASSWORD': 'your_password',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# uncomment if you need to use nodeshot.extra.oldimporter
#if 'test' not in sys.argv:
#    DATABASES['old_nodeshot'] = {
#       'ENGINE': 'django.db.backends.mysql',  # might be also postgresql or sqlite
#       'NAME': 'nodeshot',
#       'USER': 'nodeshot-readonly',
#       'PASSWORD': '*********',
#       'HOST': 'remote-ip',
#       'PORT': 'remote-port',
#    }
#    DATABASE_ROUTERS = [
#        'nodeshot.extra.oldimporter.db.DefaultRouter',
#        'nodeshot.extra.oldimporter.db.OldNodeshotRouter'
#    ]


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Rome'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

SITE_ID = 1
PROTOCOL = 'http' if DEBUG else 'https'
DOMAIN = 'localhost'
PORT = '8000' if DEBUG else None
SITE_URL = '%s://%s' % (PROTOCOL, DOMAIN)
ALLOWED_HOSTS = [DOMAIN]  # check https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts for more info

if PORT and PORT not in ['80', '433']:
    SITE_URL = '%s:%s' % (SITE_URL, PORT)

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '%s/media/' % SITE_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '%s/media/' % SITE_URL

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '%s/static/' % SITE_ROOT

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '%s/static/' % SITE_URL

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

if PROTOCOL == 'https':
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    os.environ['HTTPS'] = 'on'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# CHANGE THIS KEY AND UNCOMMENT
# Make this unique, and don't share it with anybody.
#SECRET_KEY = 'da)t*+$)ugeyip6-#tuyy$5wf2ervc0d2n#h)qb)y5@ly$t*@w'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ninux.urls' # replace myproject with the name of your project. Default project is "ninux".

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ninux.wsgi.application'


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.request",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    
    # PostgreSQL HStore extension support
    'django_hstore',
    
    # admin site
    'grappelli.dashboard',
    'grappelli',
    'filebrowser',
    'django.contrib.admin',
    
    # --- background jobs --- #
    'djcelery_email',  # Celery Django Email Backend
    
    # nodeshot
    'nodeshot.core.api',
    'nodeshot.community.participation',  # participation must go before layers
    'nodeshot.community.mailing',        # this too
    'nodeshot.core.layers',
    'nodeshot.core.nodes',
    'nodeshot.core.cms',
    'nodeshot.core.websockets',
    'nodeshot.interoperability',
    'nodeshot.community.notifications',
    'nodeshot.community.profiles',
    'nodeshot.networking.net',
    'nodeshot.networking.links',
    'nodeshot.networking.services',
    'nodeshot.networking.hardware',
    'nodeshot.networking.connectors',
    #'nodeshot.networking.monitor',
    'nodeshot.interface',
    'nodeshot.open311',
    
    # import data from old nodeshot version 0.9
    # needs python MySQL database driver
    # run "pip install MySQL-python"
    # you might need to run also a similar command according to your own OS distribution:
    # sudo apt-get install libmysqlclient-dev
    #'nodeshot.extra.oldimporter',
    
    # 3d parthy django apps
    'rest_framework',
    'rest_framework_swagger',
    'olwidget',  # geodjango better widgets
    'south',
    'debug_toolbar',
    'smuggler',
    'reversion',
    
    # profiles and social networks
    'emailconfirmation',
    'social_auth',
    
    # other utilities
    'django_extensions',
    
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
]

if 'nodeshot.community.profiles' in INSTALLED_APPS:
    AUTH_USER_MODEL = 'profiles.Profile'

# ------ DJANGO LOGGING ------ #

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
        },
        #'file': {
        #    'level': 'INFO',
        #    'class': 'logging.FileHandler',
        #    'formatter': 'verbose',
        #    'filename': 'ninux.log'
        #},
        #'logfile': {
        #    'level':'DEBUG',
        #    'class':'logging.handlers.RotatingFileHandler',
        #    'filename': SITE_ROOT + "/debug.log",
        #    'maxBytes': 50000,
        #    'backupCount': 2,
        #    'formatter': 'custom',
        #},
    },
    'loggers': {
        #'django': {
        #    'handlers':['logfile'],
        #    'level':'DEBUG',
        #    'propagate': True,
        #},
        #'django.request': {
        #    'handlers': ['mail_admins', 'logfile'],
        #    'level': 'DEBUG',
        #    'propagate': True,
        #},
        #'nodeshot.community.mailing': {
        #    'handlers': ['logfile'],
        #    'level': 'DEBUG',
        #},
        #'nodeshot.core.layers': {
        #    'handlers': ['logfile'],
        #    'level': 'DEBUG',
        #},
        #'nodeshot.community.profiles': {
        #    'handlers': ['logfile'],
        #    'level': 'DEBUG',
        #},
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'custom': {
            'format': '%(levelname)s %(asctime)s\n%(message)s'
        },
    },
}

# ------ DJANGO CACHE ------ #

CACHES = {
    'default': {
        #'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': '%s/cache' % os.path.dirname(os.path.realpath(__file__)),
        'TIMEOUT': 172800 if not DEBUG else 300,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

# ------ EMAIL SETTINGS ------ #

# if you want a dummy SMTP server that logs outgoing emails but doesn't actually send them
# you have 2 options:
#     * python -m -smtpd -n -c DebuggingServer localhost:1025
#     * python manage.py mail_debug  (django-extensions must be installed)

#EMAIL_USE_TLS = True
EMAIL_HOST = 'localhost'
#EMAIL_HOST_USER = 'your@email.org'
#EMAIL_HOST_PASSWORD = '***********'
EMAIL_PORT = 1025 if DEBUG else 25  # 1025 if you are in development mode, while 25 is usually the production port
DEFAULT_FROM_EMAIL = 'your@email.org'

# ------ CELERY ------ #

if DEBUG:
    # this app makes it possible to use django as a queue system for celery
    # so you don't need to install RabbitQM or Redis
    # pretty cool for development, but might not suffice for production if your system is heavily used
    # our suggestion is to switch only if you start experiencing issues
    INSTALLED_APPS.append('kombu.transport.django')
    BROKER_URL = 'django://'  
    # synchronous behaviour for development
    # more info here: http://docs.celeryproject.org/en/latest/configuration.html#celery-always-eager
    CELERY_ALWAYS_EAGER = True
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
else:
    # in production the default background queue manager is Redis
    BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    BROKER_TRANSPORT_OPTIONS = {
        "visibility_timeout": 3600,  # 1 hour
        "fanout_prefix": True
    }
    # in production emails are sent in the background
    EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'

#from datetime import timedelta
#
#CELERYBEAT_SCHEDULE = {
#    'synchronize': {
#        'task': 'nodeshot.interoperability.tasks.synchronize_external_layers',
#        'schedule': timedelta(hours=12),
#    },
#    # example of how to synchronize one of the layers with a different periodicity
#    'synchronize': {
#        'task': 'nodeshot.interoperability.tasks.synchronize_external_layers',
#        'schedule': timedelta(minutes=30),
#        'args': ('layer_slug',)
#    },
#    # example of how to synchronize all layers except two layers
#    'synchronize': {
#        'task': 'nodeshot.interoperability.tasks.synchronize_external_layers',
#        'schedule': timedelta(hours=12),
#        'kwargs': { 'exclude': 'layer1-slug,layer2-slug' }
#    },
#    'purge_notifications': {
#        'task': 'nodeshot.community.notifications.tasks.purge_notifications',
#        'schedule': timedelta(days=1),
#    }
#}

# ------ NODESHOT ------ #

# https://docs.djangoproject.com/en/dev/topics/i18n/translation/
# look for (ctrl + f) 'lambda' and you'll find why the following is needed
_ = lambda s: s

NODESHOT = {
    'SETTINGS': {
        # api prefix examples:
        #   * api/
        #   * api/v1/
        # leave blank to include api urls at root level, such as /nodes/, /layers/ and so on
        'API_PREFIX': 'api/v1/',
        'ACL_GLOBAL_EDITABLE': True,
        
        # the following is an example of possible granular ACL setting that can be specified
        #'ACL_NODES_NODE_EDITABLE': False,
        
        'LAYER_TEXT_HTML': True,
        'NODE_DESCRIPTION_HTML': True,
        
        'CONTACT_INWARD_LOG': True,
        'CONTACT_INWARD_MAXLENGTH': 2000,
        'CONTACT_INWARD_MINLENGTH': 15,
        'CONTACT_INWARD_REQUIRE_AUTH': False,
        'CONTACT_OUTWARD_MAXLENGTH': 9999,
        'CONTACT_OUTWARD_MINLENGTH': 50,
        'CONTACT_OUTWARD_STEP': 20,
        'CONTACT_OUTWARD_DELAY': 10,
        'CONTACT_OUTWARD_HTML': True,  # grappelli must be in INSTALLED_APPS, otherwise it won't work
        
        'PROFILE_EMAIL_CONFIRMATION': True,
        'PROFILE_REQUIRED_FIELDS': ['email'],
        
        'ADMIN_MAP_COORDS': [41.8934, 12.4960],  # lat, lng
        'ADMIN_MAP_ZOOM': 1,  # default zoom in the admin
        
        'HSTORE': True,  #  postgresql hstore types for extra data fields
        
        'REVERSION_LAYERS': True,  # activate django reversion for layers.Layer model
        'REVERSION_NODES': True,  # activate django reversion for nodes.Node model
    },
    'CHOICES': {
        'AVAILABLE_CRONJOBS': (
            ('00', _('midnight')),
            ('04', _('04:00 AM')),
        ),
        'ACCESS_LEVELS': {
            'registered': 1,
            'community': 2,
            'trusted': 3
        },
        'APPLICATION_PROTOCOLS': (
            ('http', 'http'),
            ('https', 'https'),
            ('ftp', 'FTP'),
            ('smb', 'Samba'),
            ('afp', 'Apple File Protocol'),
            ('git', 'Git'),
        )
    },
    # default values for the application or new database objects
    'DEFAULTS': {
        'NODE_PUBLISHED': True,
        'LAYER_ZOOM': 12,
        'LAYER_MINIMUM_DISTANCE': 0,
        'MAILING_SCHEDULE_OUTWARD': False,
        'ACL_GLOBAL': 'public',
        # default access_level value for app: services, model: Login
        'ACL_SERVICES_LOGIN': 'community',
        'NOTIFICATION_BOOLEAN_FIELDS': True,
        'NOTIFICATION_DISTANCE_FIELDS': 30
    },
    'API': {
        'APPS_ENABLED': [
            'nodeshot.core.nodes',
            'nodeshot.core.layers',
            'nodeshot.core.cms',
            'nodeshot.community.profiles',
            'nodeshot.community.participation',
            'nodeshot.community.notifications',
            'nodeshot.community.mailing',
            'nodeshot.networking.net',
            'nodeshot.networking.links',
            'nodeshot.networking.services',
            'nodeshot.open311'
        ]
    },
    'INTEROPERABILITY': [
        ('nodeshot.interoperability.synchronizers.Nodeshot', 'Nodeshot'),
        ('nodeshot.interoperability.synchronizers.OpenWISP', 'OpenWISP'),
        ('nodeshot.interoperability.synchronizers.OpenWISPCitySDK', 'OpenWISPCitySDK'),
        ('nodeshot.interoperability.synchronizers.ProvinciaWIFI', 'Provincia WiFi'),
        ('nodeshot.interoperability.synchronizers.ProvinciaWIFICitySDK', 'ProvinciaWIFICitySDK'),
    ],
    'NOTIFICATIONS': {
        'TEXTS': {
            'custom': None,
            'node_created': _('A new node with name "%(name)s" has been created.'),
            'node_status_changed': _('Status of node "%(name)s" has changed from "%(old_status)s" to "%(new_status)s".'),
            'your_node_status_changed': _('Status of your node "%(name)s" changed from "%(old_status)s" to "%(new_status)s".'),
            'node_deleted': _('Node "%(name)s" with ID #%(id)s was deleted.'),
        },
        # boolean: users can only turn on or off
        # distance: users can turn off (-1), turn on for all (0) or set a range of km (n)
        'USER_SETTING': {
            'node_created':             { 'type': 'distance', 'geo_field': 'geometry' },
            'node_status_changed':      { 'type': 'distance', 'geo_field': 'geometry' },
            'node_deleted':             { 'type': 'distance', 'geo_field': 'geometry' },
            'your_node_status_changed': { 'type': 'boolean' },
        },
        'ACTIONS': {
            'node_created': "reverse('api_node_details', args=[self.related_object.slug])",
            'node_status_changed': "reverse('api_node_details', args=[self.related_object.slug])",
            'your_node_status_changed': "reverse('api_node_details', args=[self.related_object.slug])",
        },
        'DELETE_OLD': 40,  # delete notifications older than specified days
        'REGISTRARS': (
            'nodeshot.community.notifications.registrars.nodes',
        )
    },
    'WEBSOCKETS': {
        'PUBLIC_PIPE': '%s/nodeshot.websockets.public' % os.path.dirname(SITE_ROOT),
        'PRIVATE_PIPE': '%s/nodeshot.websockets.private' % os.path.dirname(SITE_ROOT),
        'DOMAIN': DOMAIN,
        'LISTENING_ADDRESS': '0.0.0.0',  # set to 127.0.0.1 to accept only local calls (used for proxying to port 80 with nginx or apache mod_proxy)
        'LISTENING_PORT': 9090,
        'REGISTRARS': (
            'nodeshot.core.websockets.registrars.nodes',   
        )
    },
    # list that will contain functions to disable and re-enable some signals
    # for large import of data notifications, websockets, participation counts and similar operations
    # might be temporarily disabled to avoid unnecessary database load
    'DISCONNECTABLE_SIGNALS': [],
    # settings for old nodeshot importer
    'OLD_IMPORTER':{
        'DEFAULT_LAYER': 30,
        'STATUS_MAPPING': {
            'a': 'active',
            'h': 'active',
            'ah': 'active',
            'p': 'potential',
            'default': 'potential'
        }
    },
    'CONNECTORS': [
        ('netengine.backends.ssh.AirOS', 'AirOS (SSH)'),
        ('netengine.backends.ssh.OpenWRT', 'OpenWRT (SSH)'),
        ('netengine.backends.snmp.AirOS', 'AirOS (SNMP)'),
    ],
    'OPEN311': {
        'METADATA': 'true',
        'TYPE': 'realtime'
    }
}

NODESHOT['DEFAULTS']['CRONJOB'] = NODESHOT['CHOICES']['AVAILABLE_CRONJOBS'][0][0]

if 'test' in sys.argv:
    NODESHOT['CONNECTORS'].append(
        ('netengine.backends.Dummy', 'Dummy')
    )

# ------ GRAPPELLI ------ #

if 'grappelli' in INSTALLED_APPS:
    GRAPPELLI_ADMIN_TITLE = 'Nodeshot Admin'
    GRAPPELLI_INDEX_DASHBOARD = 'nodeshot.dashboard.NodeshotDashboard'

# ------ DEBUG TOOLBAR ------ #

INTERNAL_IPS = ('127.0.0.1', '::1',)  # ip addresses where you want to show the debug toolbar here 
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'HIDE_DJANGO_SQL': False
}

# ------ UNIT TESTING SPEED UP ------ #

SOUTH_DATABASE_ADAPTERS = {'default': 'south.db.postgresql_psycopg2'}
SOUTH_TESTS_MIGRATE = False

if 'test' in sys.argv:
    CELERY_ALWAYS_EAGER = True
    
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
        'django.contrib.auth.hashers.SHA1PasswordHasher',
        'django.contrib.auth.hashers.PBKDF2PasswordHasher',
        'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
        'django.contrib.auth.hashers.BCryptPasswordHasher',
    )

# ------ SOCIAL AUTH SETTINGS ------ #

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    #'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'nodeshot.community.profiles.social_auth_extra.pipeline.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details'
)

SOCIAL_AUTH_ENABLED_BACKENDS = ('facebook', 'google')
FACEBOOK_APP_ID              = ''
FACEBOOK_API_SECRET          = ''

SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_UUID_LENGTH = 3
SOCIAL_AUTH_SESSION_EXPIRATION = False
SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True

FACEBOOK_EXTENDED_PERMISSIONS = ['email', 'user_about_me', 'user_birthday', 'user_hometown']

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL    = '/'
