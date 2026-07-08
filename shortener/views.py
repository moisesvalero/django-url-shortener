from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db.models import F
from django.http import HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .models import Click, Link
from .services import (
    generate_short_code,
    get_cached_link,
    get_client_ip,
    hash_ip,
    is_rate_limited,
    set_cached_link,
)


def home(request):
    links = Link.objects.filter(is_active=True)[:10]
    return render(request, "shortener/home.html", {"links": links})


@require_http_methods(["POST"])
def create(request):
    url = request.POST.get("url", "").strip()

    if not url:
        return HttpResponseBadRequest("URL es requerida")

    # Validación robusta usando URLValidator de Django
    validator = URLValidator(schemes=["http", "https"])
    try:
        validator(url)
    except ValidationError:
        return HttpResponseBadRequest("URL inválida")

    ip = get_client_ip(request)
    ip_hashed = hash_ip(ip)
    if is_rate_limited(ip_hashed):
        return HttpResponseBadRequest("Demasiadas peticiones. Espera un minuto.")

    link = Link.objects.filter(original_url=url, is_active=True).first()
    if link:
        # Asegurar que esté cacheado por si acaso
        set_cached_link(link.short_code, link.id, link.original_url)
        return render(request, "shortener/partials/_link_card.html", {"link": link})

    link = Link.objects.create(original_url=url)
    link.short_code = generate_short_code(link.id)
    link.save(update_fields=["short_code"])

    set_cached_link(link.short_code, link.id, link.original_url)

    return render(request, "shortener/partials/_link_card.html", {"link": link})


def redirect_view(request, code):
    # Intentar leer desde la caché para evitar una consulta SELECT a la base de datos
    cached_data = get_cached_link(code)
    if cached_data:
        link_id, original_url = cached_data
    else:
        try:
            link = Link.objects.get(short_code=code, is_active=True)
            link_id = link.id
            original_url = link.original_url
            set_cached_link(link.short_code, link.id, link.original_url)
        except Link.DoesNotExist:
            return HttpResponseNotFound("Link no encontrado")

    ip = get_client_ip(request)
    referer = (request.META.get("HTTP_REFERER", "") or "")[:255]

    # Registrar el clic y actualizar clicks_count de forma eficiente usando el link_id
    Click.objects.create(link_id=link_id, ip_hashed=hash_ip(ip), referer=referer)
    Link.objects.filter(id=link_id).update(clicks_count=F("clicks_count") + 1)

    return redirect(original_url)


def health(request):
    return JsonResponse({"status": "ok"})
