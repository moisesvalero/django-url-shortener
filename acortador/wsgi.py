import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "acortador.settings")

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

django_app = get_wsgi_application()

# WhiteNoise envuelve la app. En serverless (Vercel) servimos los
# archivos directamente desde STATICFILES_DIRS sin collectstatic
# (Vercel no persiste /tmp entre cold starts).
application = WhiteNoise(django_app)
for static_dir in settings.STATICFILES_DIRS:
    application.add_files(str(static_dir), prefix=settings.STATIC_URL)

# En Vercel serverless, ejecuta migrations al arrancar en frío
if os.environ.get("VERCEL") and os.environ.get("DATABASE_URL"):
    from django.core.management import call_command

    call_command("migrate", "--noinput")
