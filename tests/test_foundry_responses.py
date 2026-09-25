import json

import httpx
import pytest

from scraper.foundry_responses import FoundryResponsesModel
from scraper.state import initial_state


@pytest.mark.asyncio
async def test_foundry_decide_action_parses_output_text():
    def handler(request: httpx.Request) -> httpx.Response:
        payload = {
            "output": [
                {
                    "type": "message",
                    "content": [
                        {
                            "type": "output_text",
                            "text": json.dumps({"type": "finish", "reason": "ok"}),
                        }
                    ],
                }
            ]
        }
        return httpx.Response(200, json=payload)

    transport = httpx.MockTransport(handler)
    client = FoundryResponsesModel(
        endpoint="https://example.services.ai.azure.com",
        api_key="test",
        model="gpt-4.1-mini-2",
        transport=transport,
    )

    action = await client.decide_action(initial_state("collect data"))

    assert action.type == "finish"
    assert action.reason == "ok"
