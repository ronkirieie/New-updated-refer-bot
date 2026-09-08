from __future__ import annotations

import base64
import logging
import zlib
from typing import Any

from aiohttp import web

from db import Database
from security import normalize_ip, privacy_hash

log = logging.getLogger(__name__)
MINIAPP_HTML = zlib.decompress(base64.b64decode("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")).decode("utf-8")

class MiniAppServer:
    def __init__(self, db: Database, bot: Any, bot_token: str, hash_secret: str, ipinfo_token: str = "", trust_proxy: bool = True, max_init_data_age: int = 900, rate_window_seconds: int = 3600, max_user_attempts: int = 10, max_api_requests: int = 60, reputation_cache_seconds: int = 3600) -> None:
        self.db = db
        self.trust_proxy = trust_proxy
        self.hash_secret = hash_secret
        self.rate_window_seconds = rate_window_seconds
        self.max_api_requests = max_api_requests
        self._runner: web.AppRunner | None = None
        self._site: web.TCPSite | None = None

    async def start(self, host: str, port: int) -> None:
        app = web.Application()
        app.router.add_get('/healthz', self.health)
        app.router.add_get('/miniapp', self.miniapp)
        app.router.add_get('/api/verification/ip', self.public_ip)
        self._runner = web.AppRunner(app, access_log=None)
        await self._runner.setup()
        self._site = web.TCPSite(self._runner, host, port)
        await self._site.start()
        log.info('Telegram Mini App server listening on %s:%s', host, port)

    async def stop(self) -> None:
        if self._runner:
            await self._runner.cleanup()
            self._runner = None
            self._site = None

    @staticmethod
    async def health(_: web.Request) -> web.Response:
        return web.json_response({'ok': True})

    async def miniapp(self, _: web.Request) -> web.Response:
        response = web.Response(text=MINIAPP_HTML, content_type='text/html', charset='utf-8')
        response.headers['Cache-Control'] = 'no-store'
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' https://telegram.org 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self'; object-src 'none'; frame-ancestors https://web.telegram.org https://*.telegram.org; base-uri 'none'"
        return response

    def _client_ip(self, request: web.Request) -> str | None:
        if self.trust_proxy:
            for candidate in request.headers.get('X-Forwarded-For', '').split(','):
                normalized = normalize_ip(candidate)
                if normalized:
                    return normalized
        return normalize_ip(request.remote)

    async def public_ip(self, request: web.Request) -> web.Response:
        ip = self._client_ip(request)
        if ip is None:
            return web.json_response({'message': 'Your public IP could not be detected.'}, status=422, headers={'Cache-Control': 'no-store'})
        key = privacy_hash('miniapp-ip:' + ip, self.hash_secret) or 'miniapp-ip'
        if not await self.db.consume_rate_limit(key, self.max_api_requests, self.rate_window_seconds):
            return web.json_response({'message': 'Please wait and try again.'}, status=429, headers={'Cache-Control': 'no-store'})
        return web.json_response({'ip': ip}, headers={'Cache-Control': 'no-store'})
