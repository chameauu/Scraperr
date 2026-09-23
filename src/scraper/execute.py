from __future__ import annotations

from datetime import UTC, datetime
from time import perf_counter

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
    start = perf_counter()
    try:
        if action.type == "extract":
            if model is None:
                raise ValueError("model is required for extract action")
            records = await model.extract_data(state)
            validated = TypeAdapter(list[dict]).validate_python(records)
            duration_ms = (perf_counter() - start) * 1000
            return {
                "results": state["results"] + validated,
                "last_error": None,
                "history": state["history"]
                + [
                    {
                        "action": action.model_dump(),
                        "status": "ok",
                        "error": None,
                        "ts": datetime.now(UTC).isoformat(),
                        "duration_ms": duration_ms,
                    }
                ],
            }
        await browser.perform(action)
        duration_ms = (perf_counter() - start) * 1000
        return {
            "last_error": None,
            "history": state["history"]
            + [
                {
                    "action": action.model_dump(),
                    "status": "ok",
                    "error": None,
                    "ts": datetime.now(UTC).isoformat(),
                    "duration_ms": duration_ms,
                }
            ],
        }
    except (ValidationError, Exception) as error:  # noqa: BLE001
        duration_ms = (perf_counter() - start) * 1000
        return {
            "last_error": str(error),
            "history": state["history"]
            + [
                {
                    "action": action.model_dump(),
                    "status": "error",
                    "error": str(error),
                    "ts": datetime.now(UTC).isoformat(),
                    "duration_ms": duration_ms,
                }
            ],
        }
