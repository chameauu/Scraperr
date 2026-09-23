from __future__ import annotations

from typing import Any

import httpx


class SearxNGClient:
    def __init__(
        self,
        base_url: str,
        transport: httpx.AsyncBaseTransport | None = None,
        timeout: float = 30,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._transport = transport
        self._timeout = timeout
        self._client = httpx.AsyncClient(transport=self._transport, timeout=self._timeout)

    async def search(
        self,
        query: str,
        *,
        page: int = 1,
        categories: str | None = None,
        language: str | None = None,
        time_range: str | None = None,
        safesearch: int | None = None,
    ) -> list[dict]:
        params: dict[str, Any] = {
            "q": query,
            "format": "json",
            "pageno": page,
        }
        if categories:
            params["categories"] = categories
        if language:
            params["language"] = language
        if time_range:
            params["time_range"] = time_range
        if safesearch is not None:
            params["safesearch"] = safesearch

        resp = await self._client.get(f"{self._base_url}/search", params=params)
        resp.raise_for_status()
        data = resp.json()
        return data.get("results", [])

    async def aclose(self) -> None:
        await self._client.aclose()
