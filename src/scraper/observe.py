from __future__ import annotations

import asyncio
from datetime import UTC, datetime

from .browser import BrowserAdapter
from .observation import build_compact_observation
from .state import GraphState


async def observe(
    browser: BrowserAdapter, state: GraphState, *, timeout_s: float | None = None
) -> dict:
    timeout_ms = int(timeout_s * 1000) if timeout_s is not None else None
    if timeout_s is None:
        snapshot = await browser.snapshot()
    else:
        try:
            snapshot = await asyncio.wait_for(
                browser.snapshot(timeout_ms=timeout_ms), timeout=timeout_s
            )
        except TypeError:
            snapshot = await asyncio.wait_for(browser.snapshot(), timeout=timeout_s)
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
        "last_error": None,
    }
