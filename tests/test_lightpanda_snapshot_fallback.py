import pytest

from scraper.browser.lightpanda import LightpandaBrowser


@pytest.mark.asyncio
async def test_snapshot_fallback_uses_timeout(monkeypatch):
    browser = LightpandaBrowser("http://localhost:9222", navigation_timeout_ms=1000)

    class FakePage:
        def __init__(self):
            self.called = []

        async def content(self):
            self.called.append("content")
            raise TimeoutError("content timeout")

        async def wait_for_load_state(self, _state, timeout):
            self.called.append(("wait_for_load_state", timeout))

    fake_page = FakePage()
    browser._page = fake_page  # test seam

    with pytest.raises(TimeoutError):
        await browser.snapshot(timeout_ms=10)

    assert ("wait_for_load_state", 10) in fake_page.called
