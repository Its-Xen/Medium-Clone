# when we write N o q a it means we tell linter to ignore this line
from .base import * # noqa
from .base import env

# we need to generate secret key rather that default one 
# python -c "import secrets; print(secrets.token_urlsafe(38))"
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="mCSjva91Ky2SII6PB0DqTNax9p65XOn8jiFqUt3ph4iE1GzkMm0",
)

DEBUG = True

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]