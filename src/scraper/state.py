from __future__ import annotations

from typing import Any, List, Optional
from typing_extensions import TypedDict


class GraphState(TypedDict):
    task: str
    schema: Optional[dict]
    step: int
    max_steps: int
    retries: int
    max_retries: int
    observations: List[str]
    actions: List[dict]
    results: List[dict]
    last_action: Optional[dict]
    last_error: Optional[str]
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
        "results": [],
        "last_action": None,
        "last_error": None,
        "status": "running",
    }
