import httpx
import pytest

from scraper.search import SearxNGClient


@pytest.mark.asyncio
async def test_searxng_client_returns_results():
    def handler(request: httpx.Request) -> httpx.Response:
        payload = {
            "results": [
                {"url": "https://example.com", "title": "Example"},
                {"url": "https://example.org", "title": "Example Org"},
            ]
        }
        return httpx.Response(200, json=payload)

    transport = httpx.MockTransport(handler)
    client = SearxNGClient(base_url="https://search.example", transport=transport)

    results = await client.search("test query")

    assert results[0]["url"] == "https://example.com"


@pytest.mark.asyncio
async def test_searxng_client_raises_on_http_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, json={"error": "forbidden"})

    transport = httpx.MockTransport(handler)
    client = SearxNGClient(base_url="https://search.example", transport=transport)

    with pytest.raises(httpx.HTTPStatusError):
        await client.search("test query")
