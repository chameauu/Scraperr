import asyncio

import pytest

from scraper.observe import observe
from scraper.state import initial_state


class HangingBrowser:
    async def snapshot(self) -> str:
        await asyncio.sleep(10)
        return "<html>never</html>"


@pytest.mark.asyncio
async def test_observe_times_out():
    state = initial_state("collect data")

    with pytest.raises(asyncio.TimeoutError):
        await observe(HangingBrowser(), state, timeout_s=0.01)
