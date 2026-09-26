import pytest

from scraper.observe import observe
from scraper.state import initial_state


class FakeBrowser:
    async def snapshot(self) -> str:
        return "<html>snapshot</html>"


@pytest.mark.asyncio
async def test_observation_history_records_snapshot():
    state = initial_state("collect data")
    updates = await observe(FakeBrowser(), state)

    assert updates["observations"][-1] == "snapshot"
    assert updates["observation_history"][-1]["snapshot"] == "<html>snapshot</html>"
    assert "ts" in updates["observation_history"][-1]
    compact = updates["observation_history"][-1]["compact"]
    assert "compact" in updates["observation_history"][-1]
    assert "links" in compact
    assert "buttons" in compact
    assert "inputs" in compact
