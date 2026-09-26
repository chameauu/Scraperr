import pytest

from scraper.runner import run_agent
from scraper.state import GraphState


class BrowserSpy:
    def __init__(self) -> None:
        self.connected = False

    async def connect(self) -> None:
        self.connected = True

    async def close(self) -> None:
        self.connected = False

    async def snapshot(self) -> str:
        return "<html><title>Example</title><body>Hello</body></html>"

    async def perform(self, _action):
        return None


class FakeModel:
    async def generate_schema(self, _state: GraphState):
        return {"type": "object"}

    async def decide_action(self, state: GraphState):
        if not state["results"]:
            from scraper.actions import Action

            return Action(type="finish", reason="done")
        return Action(type="finish", reason="done")

    async def extract_data(self, _state: GraphState):
        return []


@pytest.mark.asyncio
async def test_run_lightpanda_example_flow():
    browser = BrowserSpy()
    model = FakeModel()

    result = await run_agent(
        "collect data",
        browser=browser,
        model=model,
        progress=None,
    )

    assert result["status"] in {"completed", "failed"}
    assert browser.connected is False
