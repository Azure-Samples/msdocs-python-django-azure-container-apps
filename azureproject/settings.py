from pathlib import Path
import os 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Use this py command to create secret 
# python -c 'import secrets; print(secrets.token_hex())'
# SECRET_KEY = os.getenv('SECRET_KEY')

# Application definition
INSTALLED_APPS = [
    'restaurant_review.apps.RestaurantReviewConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [                                                                   
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',                      
    'django.middleware.common.CommonMiddleware',                                 
    'django.middleware.csrf.CsrfViewMiddleware',                                 
    'django.contrib.auth.middleware.AuthenticationMiddleware',                   
    'django.contrib.messages.middleware.MessageMiddleware',                      
    'django.middleware.clickjacking.XFrameOptionsMiddleware',                    
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = (str(BASE_DIR.joinpath('static')),)
STATIC_ROOT = str(BASE_DIR.joinpath('staticfiles'))

WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True
WHITENOISE_MANIFEST_STRICT = False

ROOT_URLCONF = 'azureproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

WSGI_APPLICATION = 'azureproject.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if 'RUNNING_IN_PRODUCTION' in os.environ:
    # Configure allowed host names that can be served and trusted origins for Azure Container Apps.
    ALLOWED_HOSTS = ['.azurecontainerapps.io']
    CSRF_TRUSTED_ORIGINS = ['https://*.azurecontainerapps.io']
    DEBUG = False
    DEBUG_PROPAGATE_EXCEPTIONS = True

    # SECURITY WARNING: keep the secret key used in production secret!
    # Use this py command to create secret 
    # python -c 'import secrets; print(secrets.token_hex())'
    SECRET_KEY = os.getenv('AZURE_SECRET_KEY')

    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

    # Configure database connection for Azure PostgreSQL Flexible server instance.
    # AZURE_POSTGRESQL_HOST is the full URL.
    # AZURE_POSTGRESQL_USERNAME is just name without @server-name.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['AZURE_POSTGRESQL_DATABASE'],
            'HOST': os.environ['AZURE_POSTGRESQL_HOST'],
            'USER': os.environ['AZURE_POSTGRESQL_USERNAME'],
            'PASSWORD': os.environ['AZURE_POSTGRESQL_PASSWORD'], 
        }
    }
else:
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    # Use this py command to create secret 
    # python -c 'import secrets; print(secrets.token_hex())'
    SECRET_KEY = os.getenv('LOCAL_SECRET_KEY')

    # Don't use Whitenoise to avoid having to run collectstatic first.
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

    ALLOWED_HOSTS = ['*']

    # Configure connection setting for PostgreSQL instance.
    # Set these environment variables in the .env file for this project.  
    if 'USE_REMOTE_POSTGRESQL' in os.environ:
        # Configure database connection for remote PostgreSQL instance.
        DBNAME=os.environ['AZURE_POSTGRESQL_DATABASE']
        DBHOST=os.environ['AZURE_POSTGRESQL_HOST']
        DBUSER=os.environ['AZURE_POSTGRESQL_USERNAME']
        DBPASS=os.environ['AZURE_POSTGRESQL_PASSWORD']
    else:
        # Local to instance settings.
        DBHOST=os.environ['LOCAL_HOST']
        DBNAME=os.environ['LOCAL_DATABASE']
        DBUSER=os.environ['LOCAL_USERNAME']
        DBPASS=os.environ['LOCAL_PASSWORD']

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': DBNAME,
            'HOST': DBHOST,
            'USER': DBUSER,
            'PASSWORD': DBPASS,
        }
    }
