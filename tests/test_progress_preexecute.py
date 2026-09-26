import pytest

from scraper.actions import Action
from scraper.graph import build_graph
from scraper.state import initial_state


class FakeBrowser:
    async def snapshot(self) -> str:
        return "<html>ok</html>"

    async def perform(self, _action: Action) -> None:
        return None


@pytest.mark.asyncio
async def test_progress_emits_before_execute():
    events: list[dict] = []

    async def decide(_state):
        return Action(type="navigate", target="https://example.com")

    async def progress(event: dict) -> None:
        events.append(event)

    graph = build_graph(FakeBrowser(), decide, model=None, progress=progress)
    state = initial_state("collect data")
    state["schema"] = {"type": "object"}
    await graph.ainvoke(state)

    kinds = [event.get("kind") for event in events]
    assert "pre_execute" in kinds
