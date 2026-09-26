from __future__ import annotations

from typing_extensions import TypedDict


class GraphState(TypedDict):
    task: str
    start_url: str | None
    schema: dict | None
    step: int
    max_steps: int
    retries: int
    max_retries: int
    observations: list[str]
    observation_history: list[dict]
    actions: list[dict]
    history: list[dict]
    results: list[dict]
    search_results: list[dict]
    last_action: dict | None
    last_error: str | None
    stop_reason: str | None
    status: str  # running | completed | failed


def initial_state(
    task: str,
    max_steps: int = 20,
    max_retries: int = 2,
    start_url: str | None = None,
) -> GraphState:
    return {
        "task": task,
        "start_url": start_url,
        "schema": None,
        "step": 0,
        "max_steps": max_steps,
        "retries": 0,
        "max_retries": max_retries,
        "observations": [],
        "observation_history": [],
        "actions": [],
        "history": [],
        "results": [],
        "search_results": [],
        "last_action": None,
        "last_error": None,
        "stop_reason": None,
        "status": "running",
    }
