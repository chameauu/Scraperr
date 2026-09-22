import json

import httpx
import pytest

from scraper.openai_compatible import OpenAICompatibleModel
from scraper.state import initial_state


@pytest.mark.asyncio
async def test_generate_schema_returns_dict():
    def handler(request: httpx.Request) -> httpx.Response:
        payload = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "type": "object",
                                "properties": {"title": {"type": "string"}},
                            }
                        )
                    }
                }
            ]
        }
        return httpx.Response(200, json=payload)

    transport = httpx.MockTransport(handler)

    model = OpenAICompatibleModel(
        base_url="https://example.com",
        api_key="test",
        model="gpt-test",
        transport=transport,
    )

    schema = await model.generate_schema(initial_state("collect data"))

    assert schema["type"] == "object"
    assert schema["properties"]["title"]["type"] == "string"
