import httpx
import pytest

from scraper.openai_compatible import OpenAICompatibleModel
from scraper.state import initial_state


@pytest.mark.asyncio
async def test_openai_compatible_raises_on_http_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "fail"})

    transport = httpx.MockTransport(handler)
    model = OpenAICompatibleModel(
        base_url="https://example.com",
        api_key="test",
        model="gpt-test",
        transport=transport,
    )

    with pytest.raises(httpx.HTTPStatusError):
        await model.generate_schema(initial_state("collect data"))
