import os
from .settings import *

# Configure allowed host names that can be served and trusted origins for Azure Container Apps.
ALLOWED_HOSTS = ['.azurecontainerapps.io'] if 'RUNNING_IN_PRODUCTION' in os.environ else []
CSRF_TRUSTED_ORIGINS = ['https://*.azurecontainerapps.io'] if 'RUNNING_IN_PRODUCTION' in os.environ else []
DEBUG = False
DEBUG_PROPAGATE_EXCEPTIONS = True

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