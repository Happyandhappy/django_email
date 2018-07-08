"""
WSGI config for vhodove project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys
sys.path.append('/var/www/vhodove.bg/system/root')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vhodove.settings")

import django
from django.core.handlers.wsgi import WSGIHandler


def get_wsgi_application():
    django.setup()
    return WSGIHandler()

#from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
