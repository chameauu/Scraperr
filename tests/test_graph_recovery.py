import pytest

from scraper.actions import Action
from scraper.graph import build_graph
from scraper.state import initial_state


class FlakyBrowser:
    def __init__(self):
        self.calls = 0

    async def snapshot(self) -> str:
        return "<html>try</html>"

    async def perform(self, action: Action) -> None:
        self.calls += 1
        if self.calls == 1:
            raise RuntimeError("click failed")
        return None


@pytest.mark.asyncio
async def test_graph_recovers_after_failure():
    browser = FlakyBrowser()

    async def decide(state):
        if state["retries"] == 0:
            return Action(type="click", target="#next")
        return Action(type="finish")

    graph = build_graph(browser, decide)
    result = await graph.ainvoke(initial_state("collect data", max_retries=2))

    assert result["status"] == "completed"
    assert result["retries"] == 1
