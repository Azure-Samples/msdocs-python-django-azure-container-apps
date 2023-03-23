import os
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SECRET_KEY = os.getenv('LOCAL_SECRET_KEY')

# Don't use Whitenoise to avoid having to run collectstatic first.
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

ALLOWED_HOSTS = ['*']

# Configure connection setting for local PostgreSQL instance.
# Set these environment variables in the .env file for this project.  

# Local to instance settings.
DBHOST=os.environ['LOCAL_HOST']
DBNAME=os.environ['LOCAL_DATABASE']
DBUSER=os.environ['LOCAL_USERNAME']
DBPASS=os.environ['LOCAL_PASSWORD']

# Configure database connection for remote PostgreSQL instance.
if 'USE_REMOTE_POSTGRESQL' in os.environ:
    DBNAME=os.environ['AZURE_POSTGRESQL_DATABASE']
    DBHOST=os.environ['AZURE_POSTGRESQL_HOST']
    DBUSER=os.environ['AZURE_POSTGRESQL_USERNAME']
    DBPASS=os.environ['AZURE_POSTGRESQL_PASSWORD']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DBNAME,
        'HOST': DBHOST,
        'USER': DBUSER,
        'PASSWORD': DBPASS,
    }
}
