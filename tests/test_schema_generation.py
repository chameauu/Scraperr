import pytest

from scraper.actions import Action
from scraper.graph import build_graph
from scraper.state import initial_state


class FakeModel:
    async def decide_action(self, _state):
        return Action(type="extract")

    async def generate_schema(self, _state):
        return {"type": "object", "properties": {"name": {"type": "string"}}}


class FakeBrowser:
    async def snapshot(self) -> str:
        return "<html>schema</html>"

    async def perform(self, action: Action) -> None:
        return None


@pytest.mark.asyncio
async def test_schema_can_be_injected_into_state():
    browser = FakeBrowser()
    model = FakeModel()

    async def decide(state):
        if state["schema"] is None:
            return Action(type="extract")
        return Action(type="finish")

    graph = build_graph(browser, decide, model=model)
    state = initial_state("collect data")
    state["schema"] = {"type": "object", "properties": {"name": {"type": "string"}}}

    result = await graph.ainvoke(state)
    assert result["schema"]["type"] == "object"
