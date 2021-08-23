"""
WSGI config for makefriends project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "makefriends.settings")
profile = os.environ.get("TYPEIDEA_PROFILE", 'production')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "makefriends.settings.%s" % profile)
application = get_wsgi_application()
