from __future__ import annotations

from .actions import Action
from .browser import BrowserAdapter
from .state import GraphState


async def execute_action(browser: BrowserAdapter, state: GraphState, action: Action) -> dict:
    try:
        await browser.perform(action)
        return {"last_error": None}
    except Exception as error:  # noqa: BLE001
        return {"last_error": str(error)}
