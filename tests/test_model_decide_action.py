import json

import httpx
import pytest

from scraper.openai_compatible import OpenAICompatibleModel
from scraper.state import initial_state


@pytest.mark.asyncio
async def test_decide_action_parses_action():
    def handler(request: httpx.Request) -> httpx.Response:
        payload = {
            "choices": [{"message": {"content": json.dumps({"type": "finish", "reason": "done"})}}]
        }
        return httpx.Response(200, json=payload)

    transport = httpx.MockTransport(handler)

    model = OpenAICompatibleModel(
        base_url="https://example.com",
        api_key="test",
        model="gpt-test",
        transport=transport,
    )

    action = await model.decide_action(initial_state("collect data"))

    assert action.type == "finish"
    assert action.reason == "done"
