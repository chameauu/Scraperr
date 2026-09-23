from __future__ import annotations

from datetime import UTC, datetime
from time import perf_counter

from pydantic import TypeAdapter, ValidationError

from .actions import Action
from .browser import BrowserAdapter
from .model import ModelClient
from .safety import is_safe_url
from .search import SearxNGClient
from .state import GraphState


async def execute_action(
    browser: BrowserAdapter,
    state: GraphState,
    action: Action,
    model: ModelClient | None = None,
    search_client: SearxNGClient | None = None,
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
        if action.type == "search":
            if search_client is None:
                raise ValueError("search_client is required for search action")
            if not action.value:
                raise ValueError("search query is required")
            results = await search_client.search(action.value)
            duration_ms = (perf_counter() - start) * 1000
            return {
                "search_results": state["search_results"] + results,
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
        if action.type == "navigate" and (action.target is None or not is_safe_url(action.target)):
            raise ValueError("Unsafe or invalid navigation target")
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
