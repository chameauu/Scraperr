import pytest

from scraper.actions import Action
from scraper.graph import build_graph
from scraper.state import initial_state


class FakeBrowser:
    async def snapshot(self) -> str:
        return "<html>ok</html>"

    async def perform(self, action: Action) -> None:
        return None


@pytest.mark.asyncio
async def test_graph_happy_path_finishes():
    browser = FakeBrowser()

    async def decide(_state):
        if not _state["results"]:
            return Action(type="extract")
        return Action(type="finish", reason="done")

    graph = build_graph(browser, decide, model=None)
    state = initial_state("collect data")
    state["results"] = [{"title": "A"}]
    result = await graph.ainvoke(state)

    assert result["status"] == "completed"
    assert result["actions"][-1]["type"] == "finish"
