import pytest

from scraper.runtime import agent_runtime


class BrowserSpy:
    def __init__(self) -> None:
        self.calls: list[str] = []

    async def connect(self) -> None:
        self.calls.append("connect")

    async def close(self) -> None:
        self.calls.append("close")


@pytest.mark.asyncio
async def test_agent_runtime_connects_and_closes_browser():
    browser = BrowserSpy()

    async with agent_runtime(browser=browser):
        assert browser.calls == ["connect"]

    assert browser.calls == ["connect", "close"]
