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


class ErrorBrowser:
    async def snapshot(self) -> str:
        return "<html>ok</html>"

    async def perform(self, _action: Action) -> None:
        raise RuntimeError("boom")


@pytest.mark.asyncio
async def test_history_records_successful_action():
    state = initial_state("collect data")
    action = Action(type="click", target="#ok")

    updates = await execute_action(NoopBrowser(), state, action)

    assert updates["history"][-1]["status"] == "ok"
    assert updates["history"][-1]["action"]["type"] == "click"


@pytest.mark.asyncio
async def test_history_records_extract_action():
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

    assert updates["history"][-1]["status"] == "ok"
    assert updates["history"][-1]["action"]["type"] == "extract"


@pytest.mark.asyncio
async def test_history_records_error_action():
    state = initial_state("collect data")
    action = Action(type="click", target="#ok")

    updates = await execute_action(ErrorBrowser(), state, action)

    assert updates["history"][-1]["status"] == "error"
    assert updates["history"][-1]["error"] == "boom"
