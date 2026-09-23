from __future__ import annotations

from datetime import UTC, datetime

from .browser import BrowserAdapter
from .observation import build_compact_observation
from .state import GraphState


async def observe(browser: BrowserAdapter, state: GraphState) -> dict:
    snapshot = await browser.snapshot()
    compact = build_compact_observation(snapshot)
    return {
        "observations": state["observations"] + [compact.text_snippet],
        "observation_history": state["observation_history"]
        + [
            {
                "ts": datetime.now(UTC).isoformat(),
                "snapshot": snapshot,
                "compact": {
                    "title": compact.title,
                    "links": compact.links,
                    "buttons": compact.buttons,
                    "inputs": compact.inputs,
                    "text_snippet": compact.text_snippet,
                },
            }
        ],
        "step": state["step"] + 1,
    }
