import os
from pathlib import Path

import django
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "acortador.settings")

django_app = get_wsgi_application()

# WhiteNoise envuelve la app. En serverless (Vercel) servimos los
# archivos directamente desde STATICFILES_DIRS sin collectstatic
# (Vercel no persiste /tmp entre cold starts).
application = WhiteNoise(django_app)
for static_dir in settings.STATICFILES_DIRS:
    application.add_files(str(static_dir), prefix=settings.STATIC_URL)

# Django admin tiene sus propios estáticos en el paquete Python. En
# Vercel viven en /var/task/_vendor/django/contrib/admin/static/admin/
# y en local en el venv. WhiteNoise los sirve bajo el prefijo /static/admin/.
_admin_static = Path(django.__file__).parent / "contrib" / "admin" / "static" / "admin"
if _admin_static.is_dir():
    application.add_files(str(_admin_static), prefix="static/admin/")

# En Vercel serverless, ejecuta migrations al arrancar en frío
if os.environ.get("VERCEL") and os.environ.get("DATABASE_URL"):
    from django.core.management import call_command

    call_command("migrate", "--noinput")
