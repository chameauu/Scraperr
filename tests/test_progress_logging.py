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
async def test_progress_callback_receives_events():
    events: list[dict] = []

    async def decide(_state):
        return Action(type="finish", reason="done")

    async def progress(event: dict) -> None:
        events.append(event)

    graph = build_graph(FakeBrowser(), decide, model=None, progress=progress)
    state = initial_state("collect data")
    state["results"] = [{"title": "A"}]
    state["schema"] = {"type": "object"}

    await graph.ainvoke(state)

    kinds = {event.get("kind") for event in events}
    assert "observe" in kinds
    assert "decide" in kinds
    assert "execute" in kinds
    assert "validate" in kinds
