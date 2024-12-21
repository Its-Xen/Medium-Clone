import os

from django.core.wsgi import get_wsgi_application

# TODO: change this in production
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medium.settings.local")

application = get_wsgi_application()
