import os
import secrets

from .get_token import get_token
from .settings import *

# Configure allowed host names that can be served and trusted origins for Azure Container Apps.
ALLOWED_HOSTS = ['.azurecontainerapps.io'] if 'RUNNING_IN_PRODUCTION' in os.environ else []
CSRF_TRUSTED_ORIGINS = ['https://*.azurecontainerapps.io'] if 'RUNNING_IN_PRODUCTION' in os.environ else []
DEBUG = False
DEBUG_PROPAGATE_EXCEPTIONS = True

# SECURITY WARNING: keep the secret key used in production secret!
# Use this py command to create secret 
# python -c 'import secrets; print(secrets.token_hex())'
SECRET_KEY = os.getenv('AZURE_SECRET_KEY') or secrets.token_hex()

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Configure database connection for Azure PostgreSQL Flexible server instance.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DBNAME'],
        'HOST': os.environ['DBHOST'] + ".postgres.database.azure.com",
        'USER': os.environ['DBUSER'],
        'PASSWORD': 'mickey'
    }
}
get_token()
