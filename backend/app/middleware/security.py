"""
JurisPulse — Security Headers Middleware
==========================================
Adds defensive HTTP security headers to every response.
These headers harden the API against common web attacks.
"""

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.config.settings import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Adds the following headers to every response:

    - Strict-Transport-Security: Enforce HTTPS (1 year)
    - X-Content-Type-Options: Prevent MIME sniffing
    - X-Frame-Options: Clickjacking protection
    - X-XSS-Protection: Legacy XSS filter (belt-and-suspenders)
    - Referrer-Policy: Control referrer header leakage
    - Permissions-Policy: Disable unneeded browser features
    - Content-Security-Policy: Restrict resource loading
    - Cache-Control: Prevent caching of API responses
    """

    _SECURITY_HEADERS = {
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": (
            "geolocation=(), microphone=(), camera=(), payment=(), usb=()"
        ),
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Pragma": "no-cache",
    }

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        response = await call_next(request)

        if settings.SECURITY_HEADERS_ENABLED:
            for header, value in self._SECURITY_HEADERS.items():
                response.headers[header] = value
            response.headers["Content-Security-Policy"] = (
                settings.CONTENT_SECURITY_POLICY
            )

        # Remove server identification headers to reduce information leakage
        if "server" in response.headers:
            del response.headers["server"]
        if "x-powered-by" in response.headers:
            del response.headers["x-powered-by"]

        return response
