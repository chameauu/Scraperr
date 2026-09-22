import json

import httpx
import pytest

from scraper.actions import Action
from scraper.execute import execute_action
from scraper.openai_compatible import OpenAICompatibleModel
from scraper.state import initial_state


class NoopBrowser:
    async def snapshot(self) -> str:
        return "<html>ok</html>"

    async def perform(self, _action: Action) -> None:
        return None


@pytest.mark.asyncio
async def test_extract_action_appends_results():
    def handler(request: httpx.Request) -> httpx.Response:
        payload = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            [
                                {"title": "A"},
                                {"title": "B"},
                            ]
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

    state = initial_state("collect data")
    action = Action(type="extract")
    updates = await execute_action(NoopBrowser(), state, action, model=model)

    assert updates["results"] == [{"title": "A"}, {"title": "B"}]
    assert updates["last_error"] is None


@pytest.mark.asyncio
async def test_extract_action_rejects_invalid_shape():
    def handler(request: httpx.Request) -> httpx.Response:
        payload = {"choices": [{"message": {"content": json.dumps({"title": "not a list"})}}]}
        return httpx.Response(200, json=payload)

    transport = httpx.MockTransport(handler)
    model = OpenAICompatibleModel(
        base_url="https://example.com",
        api_key="test",
        model="gpt-test",
        transport=transport,
    )

    state = initial_state("collect data")
    action = Action(type="extract")
    updates = await execute_action(NoopBrowser(), state, action, model=model)

    assert updates["last_error"] is not None
