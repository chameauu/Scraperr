from __future__ import annotations

from .browser import BrowserAdapter
from .state import GraphState


async def observe(browser: BrowserAdapter, state: GraphState) -> dict:
    snapshot = await browser.snapshot()
    return {
        "observations": state["observations"] + [snapshot],
        "step": state["step"] + 1,
    }
