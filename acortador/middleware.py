import secrets


class ContentSecurityPolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        nonce = secrets.token_hex(32)
        request.csp_nonce = nonce

        response = self.get_response(request)

        csp = (
            f"default-src 'self'; "
            f"script-src 'self' https://unpkg.com 'nonce-{nonce}'; "
            f"style-src 'self' https://fonts.googleapis.com 'unsafe-inline'; "
            f"font-src 'self' https://fonts.gstatic.com; "
            f"img-src 'self' data:; "
            f"connect-src 'self'; "
            f"frame-ancestors 'none'; "
            f"form-action 'self'; "
            f"base-uri 'self'"
        )

        response["Content-Security-Policy"] = csp
        return response
