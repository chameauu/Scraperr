import pytest

from scraper.actions import Action
from scraper.graph import build_graph
from scraper.state import initial_state


class FakeBrowser:
    async def snapshot(self) -> str:
        return "<html>schema</html>"

    async def perform(self, action: Action) -> None:
        return None


class FakeModel:
    async def decide_action(self, _state):
        return Action(type="extract")

    async def generate_schema(self, _state):
        return {"type": "object", "properties": {"title": {"type": "string"}}}


@pytest.mark.asyncio
async def test_schema_node_generates_schema_when_missing():
    browser = FakeBrowser()
    model = FakeModel()

    async def decide(_state):
        return Action(type="finish")

    graph = build_graph(browser, decide, model=model)
    result = await graph.ainvoke(initial_state("collect data"))

    assert result["schema"]["properties"]["title"]["type"] == "string"
