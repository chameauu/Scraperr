import pytest

from scraper.actions import Action
from scraper.graph import build_graph
from scraper.state import initial_state


class BrowserSpy:
    def __init__(self) -> None:
        self.actions: list[Action] = []

    async def snapshot(self) -> str:
        return "<html>ok</html>"

    async def perform(self, action: Action) -> None:
        self.actions.append(action)


@pytest.mark.asyncio
async def test_graph_navigates_start_url_before_observe():
    browser = BrowserSpy()

    async def decide(_state):
        return Action(type="finish", reason="done")

    graph = build_graph(browser, decide, model=None)
    state = initial_state("collect data", start_url="https://example.com")
    result = await graph.ainvoke(state)

    assert browser.actions
    assert browser.actions[0].type == "navigate"
    assert browser.actions[0].target == "https://example.com"
    assert result["actions"][0]["type"] == "navigate"
