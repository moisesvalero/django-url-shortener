from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path

security_txt = (
    "Contact: https://moisesvalero.es/contact\n"
    "Preferred-Languages: es, en\n"
    "Canonical: https://acortador.moisesvalero.es/.well-known/security.txt\n"
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        ".well-known/security.txt",
        lambda r: HttpResponse(security_txt, content_type="text/plain"),
    ),
    path(
        "robots.txt",
        lambda r: HttpResponse(
            "User-agent: *\nDisallow: /admin/\n",
            content_type="text/plain",
        ),
    ),
    path(
        "llms.txt",
        lambda r: HttpResponse(
            "# URL Shortener\n\n"
            "## Acortador de URLs rápido y seguro.\n\n"
            "Crea enlaces cortos, rastrea clics y simplifica tu presencia digital.\n\n"
            "## Páginas\n\n"
            "- Inicio: https://acortador.moisesvalero.es/\n"
            "- Estado: https://acortador.moisesvalero.es/health\n"
            "- Contacto: https://moisesvalero.es/contact\n"
            "- Admin: https://acortador.moisesvalero.es/admin/\n"
            "- Info extendida: https://acortador.moisesvalero.es/llms-full.txt\n",
            content_type="text/plain",
        ),
    ),
    path(
        "llms-full.txt",
        lambda r: HttpResponse(
            "# URL Shortener — Documentación completa\n\n"
            "Url shortener construido con Django 5.2, HTMX y Tailwind CSS.\n"
            "Desplegado en Vercel. Código abierto en GitHub.\n\n"
            "## Funcionalidades\n\n"
            "- Acortar URLs largas en códigos cortos (base62)\n"
            "- Redirección instantánea con contador de clics\n"
            "- Rate limiting por IP\n"
            "- Cache en memoria para redirecciones rápidas\n"
            "- Panel de administración Jazzmin\n"
            "- Diseño responsive con modo oscuro\n"
            "- HTMX para interacciones sin recarga\n\n"
            "## Stack técnico\n\n"
            "- Backend: Django 5.2 + SQLite / PostgreSQL\n"
            "- Frontend: HTMX 2.0 + Tailwind CSS 3\n"
            "- Servidor: Gunicorn + WhiteNoise\n"
            "- Despliegue: Vercel (@vercel/python)\n"
            "- Tooling: uv + ruff + pytest\n\n"
            "## Páginas\n\n"
            "- Inicio (acortar): https://acortador.moisesvalero.es/\n"
            "- Estado/health: https://acortador.moisesvalero.es/health\n"
            "- Admin: https://acortador.moisesvalero.es/admin/\n"
            "- Portfolio: https://moisesvalero.es\n\n"
            "## API endpoints\n\n"
            "- POST /create — Crea un url corto (body: url)\n"
            "- GET /health — Health check JSON\n"
            "- GET /{code} — Redirige al destino\n\n"
            "## Contacto\n\n"
            "- Web: https://moisesvalero.es\n"
            "- Issues: https://github.com/moisesvalero/django-url-shortener\n",
            content_type="text/plain",
        ),
    ),
    path("", include("shortener.urls")),
]
