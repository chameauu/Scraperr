import json

import httpx
import pytest

from scraper.graph import build_graph
from scraper.openai_compatible import OpenAICompatibleModel
from scraper.state import initial_state


class FakeBrowser:
    async def snapshot(self) -> str:
        return "<html>ok</html>"

    async def perform(self, _action) -> None:
        return None


@pytest.mark.asyncio
async def test_decide_uses_model_when_decide_is_none():
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

    graph = build_graph(FakeBrowser(), decide=None, model=model)
    result = await graph.ainvoke(initial_state("collect data"))

    assert result["actions"][-1]["type"] == "finish"
