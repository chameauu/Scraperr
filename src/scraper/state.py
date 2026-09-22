from __future__ import annotations

from typing_extensions import TypedDict


class GraphState(TypedDict):
    task: str
    schema: dict | None
    step: int
    max_steps: int
    retries: int
    max_retries: int
    observations: list[str]
    actions: list[dict]
    history: list[dict]
    results: list[dict]
    last_action: dict | None
    last_error: str | None
    status: str  # running | completed | failed


def initial_state(task: str, max_steps: int = 20, max_retries: int = 2) -> GraphState:
    return {
        "task": task,
        "schema": None,
        "step": 0,
        "max_steps": max_steps,
        "retries": 0,
        "max_retries": max_retries,
        "observations": [],
        "actions": [],
        "history": [],
        "results": [],
        "last_action": None,
        "last_error": None,
        "status": "running",
    }
