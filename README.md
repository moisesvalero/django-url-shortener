# django-url-shortener

A modern, high-performance URL shortener built with **Django 5.2**, **HTMX**, **Tailwind CSS**, and deployed on **Vercel**. Features real-time link shortening, one-click copy, click analytics, rate limiting, and lazy-loading cache.

**Live demo:** [https://a.moisesvalero.es](https://a.moisesvalero.es)

---

## Features

- **Instant link shortening** — paste a long URL, get a short one in under 200ms
- **Real-time UI** — HTMX-powered partial updates without page reloads
- **One-click copy** — copies the short URL to clipboard
- **Click analytics** — tracks every redirect with hashed IP, referrer, and timestamp
- **Rate limiting** — prevents abuse with per-IP throttling
- **Lazy caching** — stores resolved URLs in memory cache after the first hit
- **Responsive design** — mobile-first layout with Tailwind CSS
- **Dark mode** — modern dark theme with Material Design 3 color system
- **Production-ready** — Whitenoise for static files, PostgreSQL support, SSL/HTTPS enforced
- **Vercel-native** — serverless Python runtime with zero cold-boot overhead

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Django 5.2 (Python 3.12) |
| **Frontend** | HTMX 2.x, Tailwind CSS 3 |
| **Database** | PostgreSQL (Neon) / SQLite (dev) |
| **Cache** | Django LocMemCache (lazy-load) |
| **Static files** | Whitenoise |
| **Deployment** | Vercel (serverless Python) |
| **Design** | Material Design 3, Geist font, Material Symbols |

## Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────┐
│  Browser     │────▶│  Vercel Edge      │────▶│  Django App   │
│  (HTMX)      │     │  (CDN + SSL)      │     │  (WSGI)       │
└─────────────┘     └──────────────────┘     └──────┬───────┘
         ▲                                           │
         │  POST /create →                            │
         │  GET /{slug} → 302 redirect               │
         │                                           ▼
         │                                   ┌──────────────┐
         │                                   │  PostgreSQL   │
         │                                   │  (Neon)       │
         │                                   └──────────────┘
         │
         └─────────────────────────────── HTTP 302 response
```

### How it works

1. User submits a long URL via the form (HTMX `POST /create`)
2. Django validates, deduplicates, generates a short code, saves to DB
3. Response renders a card with the short URL (`https://a.moisesvalero.es/{code}`)
4. On redirect (`GET /{code}`), Django looks up the link, increments click count, returns HTTP 302
5. After the first hit, the resolved URL is cached in memory for faster subsequent lookups

## Getting Started

### Prerequisites

- Python 3.12+
- uv (Python package manager)
- Node.js + pnpm (for Tailwind CSS build)

### Local Development

```bash
# 1. Clone the repository
git clone https://github.com/moisesvalero/django-url-shortener.git
cd django-url-shortener

# 2. Install Python dependencies
uv sync

# 3. Install Tailwind CSS dependencies
pnpm install

# 4. Build Tailwind CSS
pnpm exec tailwindcss -i static/src/input.css -o static/dist/output.css --minify

# 5. Run migrations
uv run manage.py migrate

# 6. Start the development server
uv run manage.py runserver

# 7. Open http://localhost:8000
```

### Environment Variables

Create a `.env` file in the project root:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
BASE_URL=http://localhost:8000
ALLOWED_HOSTS=localhost,127.0.0.1,a.moisesvalero.es
CSRF_TRUSTED_ORIGINS=http://localhost:8000,https://a.moisesvalero.es
IP_HASH_SALT=your-salt

# PostgreSQL (optional — falls back to SQLite)
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

## Deployment

### Vercel

The project is configured for Vercel with `vercel.json`. The application runs as a serverless Python function via `@vercel/python`.

```bash
# Deploy to Vercel
vercel --prod
```

**Required environment variables on Vercel:**

| Variable | Value |
|---|---|
| `DJANGO_SECRET_KEY` | Long random secret |
| `DJANGO_DEBUG` | `False` |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1,acortador.moisesvalero.es,a.moisesvalero.es` |
| `CSRF_TRUSTED_ORIGINS` | `http://localhost:8000,https://acortador.moisesvalero.es,https://a.moisesvalero.es` |
| `BASE_URL` | `https://a.moisesvalero.es` |
| `IP_HASH_SALT` | Long random salt |
| `DATABASE_URL` | Your PostgreSQL connection string |

### Database

- **Development:** SQLite (no setup required)
- **Production:** PostgreSQL via [Neon](https://neon.tech) (free tier) or any provider

## API

### Resolve a short URL

```http
GET /api/resolve/{slug}/
```

**Response:**
```json
{
  "url": "https://example.com/very/long/url"
}
```

Returns `404` if the slug does not exist.

### Health check

```http
GET /health/
```

**Response:**
```json
{
  "status": "ok"
}
```

## Domain Setup

The application uses a custom short domain `a.moisesvalero.es` for generated short URLs. The apex domain `moisesvalero.es` is managed on Vercel, and the subdomain `a.moisesvalero.es` is added to the same Vercel project with automatic SSL certificate provisioning.

No external DNS configuration is required — Vercel handles routing and HTTPS automatically.

## Project Structure

```
django-url-shortener/
├── acortador/
│   ├── settings.py         # Django settings
│   ├── urls.py             # Root URL configuration
│   └── wsgi.py             # WSGI application
├── shortener/
│   ├── templates/          # Django templates (HTMX)
│   ├── models.py           # Link and Click models
│   ├── views.py            # URL shortening and redirect logic
│   ├── services.py         # Code generation, rate limiting, caching
│   └── context_processors.py  # BASE_URL for templates
├── static/
│   ├── src/
│   │   └── input.css       # Tailwind CSS source
│   └── dist/
│       └── output.css      # Compiled CSS
├── tests/
│   ├── test_models.py
│   ├── test_views.py
│   └── test_services.py
├── vercel.json             # Vercel deployment configuration
├── pyproject.toml           # Python dependencies and tool config
├── package.json            # Node.js dependencies (Tailwind)
├── tailwind.config.js      # Tailwind CSS configuration
└── README.md
```

## Tests

```bash
uv run pytest -v --no-header
```

The test suite covers:
- Model creation and short URL generation
- View responses and redirect behavior
- Service layer (code generation, rate limiting, caching, IP hashing)

## Linting & Formatting

```bash
# Lint
uv run ruff check .

# Format check
uv run ruff format --check .
```

## License

MIT
