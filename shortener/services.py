import hashlib

from django.conf import settings
from django.core.cache import cache

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
CODE_LENGTH = 6
ID_OFFSET = 10_000
CACHE_TIMEOUT = 600  # 10 minutos
RATE_LIMIT_WINDOW = 60  # 1 minuto
RATE_LIMIT_MAX = 10


def base62_encode(num: int) -> str:
    if num == 0:
        return BASE62[0]
    chars = []
    while num > 0:
        num, rem = divmod(num, 62)
        chars.append(BASE62[rem])
    return "".join(reversed(chars))


def generate_short_code(link_id: int) -> str:
    encoded = base62_encode(link_id + ID_OFFSET)
    return encoded.rjust(CODE_LENGTH, BASE62[0])


def get_cached_link(code: str) -> tuple[int, str] | None:
    return cache.get(f"link:{code}")


def set_cached_link(code: str, link_id: int, url: str) -> None:
    cache.set(f"link:{code}", (link_id, url), CACHE_TIMEOUT)


def invalidate_link_cache(code: str) -> None:
    cache.delete(f"link:{code}")


def hash_ip(ip: str) -> str:
    salt = settings.IP_HASH_SALT
    return hashlib.sha256(f"{ip}{salt}".encode()).hexdigest()


def get_client_ip(request) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR", "")
    return ip


def is_rate_limited(ip_hashed: str) -> bool:
    cache_key = f"rl:{ip_hashed}"
    added = cache.add(cache_key, 1, RATE_LIMIT_WINDOW)
    if not added:
        try:
            count = cache.incr(cache_key)
        except ValueError:
            # Fallback en caso de que expire justo entre add e incr
            cache.set(cache_key, 1, RATE_LIMIT_WINDOW)
            count = 1
    else:
        count = 1
    return count > RATE_LIMIT_MAX
