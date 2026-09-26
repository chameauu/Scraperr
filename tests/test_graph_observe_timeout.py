import asyncio

import pytest

from scraper.graph import build_graph
from scraper.state import initial_state


class SlowBrowser:
    async def snapshot(self) -> str:
        await asyncio.sleep(1)
        return "<html>late</html>"

    async def perform(self, _action):
        return None


@pytest.mark.asyncio
async def test_graph_fails_after_observe_timeout_retries_exhausted():
    async def decide(_state):
        raise AssertionError("decide should not be called when observe times out")

    graph = build_graph(
        SlowBrowser(),
        decide,
        model=None,
        observe_timeout_s=0.01,
    )
    state = initial_state("collect data", max_retries=0)
    result = await graph.ainvoke(state)

    assert result["status"] == "failed"
    assert result["stop_reason"] == "retries_exhausted"
    assert result["last_error"] == "observe_timeout"
