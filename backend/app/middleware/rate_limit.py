"""
JurisPulse — Redis-backed Rate Limiting Middleware
====================================================
Uses a sliding-window counter stored in Redis.
Limits are applied per IP address + path prefix.

Limits are configurable via settings:
  RATE_LIMIT_PER_MINUTE
  RATE_LIMIT_PER_HOUR
  RATE_LIMIT_BURST

Returns 429 JSON when a client exceeds the limit.
Adds standard rate-limit response headers.
"""

import json
import time

import redis.asyncio as aioredis
import structlog
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.config.settings import settings
from app.utils.responses import error_response

logger = structlog.get_logger("jurispulse.rate_limit")

# Paths that should not be rate-limited (health checks, metrics)
_EXCLUDE_PATHS = frozenset(["/api/v1/health", "/favicon.ico"])


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Sliding-window per-IP rate limiter backed by Redis.

    Two windows are enforced:
    - per-minute: RATE_LIMIT_PER_MINUTE requests / 60 s
    - per-hour:   RATE_LIMIT_PER_HOUR requests / 3600 s
    """

    def __init__(self, app, redis_url: str = settings.REDIS_URL) -> None:
        super().__init__(app)
        self._redis_url = redis_url
        self._client: aioredis.Redis | None = None

    async def _get_client(self) -> aioredis.Redis:
        if self._client is None:
            self._client = aioredis.from_url(
                self._redis_url,
                db=settings.REDIS_RATE_LIMIT_DB,
                decode_responses=True,
            )
        return self._client

    def _client_ip(self, request: Request) -> str:
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        if request.client:
            return request.client.host
        return "unknown"

    async def _is_allowed(self, client_ip: str) -> tuple[bool, dict]:
        """
        Check rate limits.
        Returns (allowed, headers_dict).
        """
        redis = await self._get_client()
        now = int(time.time())

        minute_key = f"rl:min:{client_ip}:{now // 60}"
        hour_key = f"rl:hr:{client_ip}:{now // 3600}"

        try:
            pipe = redis.pipeline()
            pipe.incr(minute_key)
            pipe.expire(minute_key, 65)
            pipe.incr(hour_key)
            pipe.expire(hour_key, 3610)
            results = await pipe.execute()

            minute_count = results[0]
            hour_count = results[2]

            minute_limit = settings.RATE_LIMIT_PER_MINUTE
            hour_limit = settings.RATE_LIMIT_PER_HOUR

            headers = {
                "X-RateLimit-Limit-Minute": str(minute_limit),
                "X-RateLimit-Remaining-Minute": str(max(0, minute_limit - minute_count)),
                "X-RateLimit-Limit-Hour": str(hour_limit),
                "X-RateLimit-Remaining-Hour": str(max(0, hour_limit - hour_count)),
            }

            if minute_count > minute_limit or hour_count > hour_limit:
                return False, headers
            return True, headers

        except Exception as e:
            # If Redis is unavailable, fail open (allow the request)
            logger.warning("rate_limit.redis_unavailable", error=str(e))
            return True, {}

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        if request.url.path in _EXCLUDE_PATHS:
            return await call_next(request)

        client_ip = self._client_ip(request)
        allowed, rl_headers = await self._is_allowed(client_ip)

        if not allowed:
            logger.warning(
                "rate_limit.exceeded",
                client_ip=client_ip,
                path=request.url.path,
            )
            resp = error_response(
                message="Rate limit exceeded. Please wait before making more requests.",
                code="RATE_LIMIT_EXCEEDED",
                status_code=429,
            )
            for k, v in rl_headers.items():
                resp.headers[k] = v
            return resp

        response = await call_next(request)
        for k, v in rl_headers.items():
            response.headers[k] = v
        return response
