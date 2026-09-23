from __future__ import annotations

from datetime import UTC, datetime

from .browser import BrowserAdapter
from .state import GraphState


async def observe(browser: BrowserAdapter, state: GraphState) -> dict:
    snapshot = await browser.snapshot()
    return {
        "observations": state["observations"] + [snapshot],
        "observation_history": state["observation_history"]
        + [
            {
                "ts": datetime.now(UTC).isoformat(),
                "snapshot": snapshot,
            }
        ],
        "step": state["step"] + 1,
    }
