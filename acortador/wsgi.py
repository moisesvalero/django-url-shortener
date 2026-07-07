import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "acortador.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# En Vercel serverless, ejecuta migrations/collectstatic al arrancar en frío
if os.environ.get("VERCEL") and os.environ.get("DATABASE_URL"):
    from django.core.management import call_command
    call_command("migrate", "--noinput")
    call_command("collectstatic", "--noinput")
