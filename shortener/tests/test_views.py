from django.test import Client, TestCase
from django.urls import reverse

from shortener.models import Link


class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_returns_200(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_uses_correct_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "shortener/home.html")

    def test_home_shows_links(self):
        Link.objects.create(original_url="https://example.com", short_code="aaaaaa")
        response = self.client.get(reverse("home"))
        self.assertContains(response, "aaaaaa")

    def test_home_empty_when_no_links(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)


class CreateViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_valid_url(self):
        response = self.client.post(
            reverse("create"),
            {"url": "https://example.com/muy-largo"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "example.com")
        self.assertEqual(Link.objects.count(), 1)

    def test_create_invalid_scheme(self):
        response = self.client.post(
            reverse("create"),
            {"url": "ftp://example.com"},
        )
        self.assertEqual(response.status_code, 400)

    def test_create_empty_url(self):
        response = self.client.post(reverse("create"), {"url": ""})
        self.assertEqual(response.status_code, 400)

    def test_create_only_get_returns_405(self):
        response = self.client.get(reverse("create"))
        self.assertEqual(response.status_code, 405)

    def test_create_duplicate_returns_same_link(self):
        self.client.post(
            reverse("create"),
            {"url": "https://example.com/dup"},
        )
        response = self.client.post(
            reverse("create"),
            {"url": "https://example.com/dup"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Link.objects.count(), 1)

    def test_create_no_url_param(self):
        response = self.client.post(reverse("create"), {})
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_url_structure(self):
        response = self.client.post(
            reverse("create"),
            {"url": "https://"},
        )
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_characters_in_url(self):
        response = self.client.post(
            reverse("create"),
            {"url": "https://invalid_url_with_spaces or_chars"},
        )
        self.assertEqual(response.status_code, 400)


class RedirectViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.link = Link.objects.create(
            original_url="https://example.com/destino",
            short_code="abc123",
        )

    def test_redirect_valid_code(self):
        response = self.client.get(f"/{self.link.short_code}")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "https://example.com/destino")

    def test_redirect_invalid_code_returns_404(self):
        response = self.client.get("/nonexistent")
        self.assertEqual(response.status_code, 404)

    def test_redirect_inactive_link_returns_404(self):
        self.link.is_active = False
        self.link.save()
        response = self.client.get(f"/{self.link.short_code}")
        self.assertEqual(response.status_code, 404)

    def test_redirect_records_click(self):
        self.client.get(f"/{self.link.short_code}")
        self.link.refresh_from_db()
        self.assertEqual(self.link.clicks_count, 1)

    def test_redirect_records_multiple_clicks(self):
        self.client.get(f"/{self.link.short_code}")
        self.client.get(f"/{self.link.short_code}")
        self.link.refresh_from_db()
        self.assertEqual(self.link.clicks_count, 2)

    def test_redirect_does_not_record_click_on_404(self):
        self.client.get("/nonexistent")
        self.link.refresh_from_db()
        self.assertEqual(self.link.clicks_count, 0)


class CacheRedirectViewTests(TestCase):
    def setUp(self):
        from django.core.cache import cache

        self.client = Client()
        cache.clear()
        self.link = Link.objects.create(
            original_url="https://example.com/cache-test",
            short_code="cache1",
        )

    def test_redirect_uses_cache(self):
        # Primera petición puebla la caché
        response = self.client.get(f"/{self.link.short_code}")
        self.assertEqual(response.status_code, 302)

        # Modificamos directamente en base de datos para simular desincronización
        self.link.original_url = "https://example.com/modified-in-db"
        self.link.save()

        # Al consultar de nuevo, debería usar el valor cacheado
        response = self.client.get(f"/{self.link.short_code}")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "https://example.com/cache-test")


class HealthViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_health_returns_ok(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
