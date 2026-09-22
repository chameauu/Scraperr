from __future__ import annotations

from pydantic import TypeAdapter, ValidationError

from .actions import Action
from .browser import BrowserAdapter
from .model import ModelClient
from .state import GraphState


async def execute_action(
    browser: BrowserAdapter,
    state: GraphState,
    action: Action,
    model: ModelClient | None = None,
) -> dict:
    try:
        if action.type == "extract":
            if model is None:
                raise ValueError("model is required for extract action")
            records = await model.extract_data(state)
            validated = TypeAdapter(list[dict]).validate_python(records)
            return {
                "results": state["results"] + validated,
                "last_error": None,
            }
        await browser.perform(action)
        return {"last_error": None}
    except (ValidationError, Exception) as error:  # noqa: BLE001
        return {"last_error": str(error)}
