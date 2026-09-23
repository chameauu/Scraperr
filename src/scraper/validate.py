from __future__ import annotations

from .state import GraphState


def validate(state: GraphState) -> dict:
    if state["last_action"] and state["last_action"].get("type") == "finish":
        return {"status": "completed"}

    if state["last_error"]:
        if state["retries"] + 1 > state["max_retries"]:
            return {"status": "failed", "stop_reason": "retries_exhausted"}
        return {"retries": state["retries"] + 1}

    if state["step"] >= state["max_steps"]:
        return {"status": "failed", "stop_reason": "max_steps_reached"}

    return {"status": "running"}
