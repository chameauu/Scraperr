import pytest

from scraper.runtime import agent_runtime


class BrowserSpy:
    async def connect(self) -> None:
        return None

    async def close(self) -> None:
        return None


@pytest.mark.asyncio
async def test_agent_runtime_emits_progress_events():
    events: list[dict] = []

    async def progress(event: dict) -> None:
        events.append(event)

    async with agent_runtime(browser=BrowserSpy(), progress=progress):
        pass

    kinds = {event.get("kind") for event in events}
    assert "runtime_connect_start" in kinds
    assert "runtime_connect_done" in kinds
