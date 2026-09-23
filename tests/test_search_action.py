import pytest

from scraper.actions import Action
from scraper.execute import execute_action
from scraper.state import initial_state


class FakeSearchClient:
    async def search(self, query: str, *, page: int = 1):
        return [
            {"url": "https://example.com", "title": "Example"},
        ]


class NoopBrowser:
    async def snapshot(self) -> str:
        return "<html>ok</html>"

    async def perform(self, _action: Action) -> None:
        return None


@pytest.mark.asyncio
async def test_search_action_appends_results():
    state = initial_state("collect data")
    action = Action(type="search", value="cats")

    updates = await execute_action(NoopBrowser(), state, action, search_client=FakeSearchClient())

    assert updates["search_results"][0]["title"] == "Example"
