"""
WSGI config for azureproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Check for the RUNNING_IN_PRODUCTION environment variable to see if we are running in Azure App Service
# If so, then load the settings from production.py
settings_module = 'azureproject.production' if 'RUNNING_IN_PRODUCTION' in os.environ else 'azureproject.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
