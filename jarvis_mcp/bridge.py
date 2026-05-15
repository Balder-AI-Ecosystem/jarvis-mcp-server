from __future__ import annotations

from typing import Any

import httpx

from .config import get_settings


class JarvisBridge:
    """HTTP client gọi tới JARVIS core API."""

    def __init__(self) -> None:
        settings = get_settings()
        self._base_url = str(settings.jarvis_core_url).rstrip("/")
        self._timeout = settings.jarvis_request_timeout

    def _headers(self) -> dict[str, str]:
        settings = get_settings()
        headers: dict[str, str] = {}
        if settings.jarvis_api_key:
            headers["X-API-Key"] = settings.jarvis_api_key
        return headers

    def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            base_url=self._base_url,
            timeout=self._timeout,
            headers=self._headers(),
        )

    async def chat(self, message: str, session_id: str | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"message": message}
        if session_id:
            payload["session_id"] = session_id
        async with self._client() as client:
            response = await client.post("/chat", json=payload)
            response.raise_for_status()
            return dict(response.json())

    async def chat_history(self, limit: int = 20) -> list[dict[str, Any]]:
        async with self._client() as client:
            response = await client.get("/chat/history", params={"limit": limit})
            response.raise_for_status()
            data = response.json()
            return list(data) if isinstance(data, list) else []

    async def health(self) -> dict[str, Any]:
        async with self._client() as client:
            response = await client.get("/health")
            response.raise_for_status()
            return dict(response.json())

    async def autonomy_status(self) -> dict[str, Any]:
        async with self._client() as client:
            response = await client.get("/autonomy/status")
            response.raise_for_status()
            return dict(response.json())

    async def autonomy_run(
        self,
        goals: list[str] | None = None,
        allow_promotion: bool = True,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"allow_promotion": allow_promotion}
        if goals:
            body["goals"] = goals
        async with self._client() as client:
            response = await client.post("/autonomy/run", json=body)
            response.raise_for_status()
            return dict(response.json())

    async def autonomy_lifecycle(self, limit: int = 10) -> list[dict[str, Any]]:
        async with self._client() as client:
            response = await client.get("/autonomy/lifecycle")
            response.raise_for_status()
            data = response.json()
            items = list(data) if isinstance(data, list) else []
            return items[:limit]

    async def knowledge_search(self, query: str, lane: str | None = None, top_k: int = 5) -> list[dict[str, Any]]:
        # Core endpoint: GET /knowledge/search?query=<str>
        # Returns list of {path, zone, source, score}
        params: dict[str, Any] = {"query": query}
        async with self._client() as client:
            response = await client.get("/knowledge/search", params=params)
            response.raise_for_status()
            data = response.json()
            hits = list(data) if isinstance(data, list) else []
            if lane:
                hits = [h for h in hits if str(h.get("zone") or "") == lane]
            return hits[:top_k]

    async def runtime_preflight(self) -> dict[str, Any]:
        async with self._client() as client:
            response = await client.get("/runtime/preflight")
            response.raise_for_status()
            return dict(response.json())


_bridge: JarvisBridge | None = None


def get_bridge() -> JarvisBridge:
    global _bridge
    if _bridge is None:
        _bridge = JarvisBridge()
    return _bridge
