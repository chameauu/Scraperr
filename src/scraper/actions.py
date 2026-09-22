from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

ActionType = Literal[
    "search",
    "navigate",
    "click",
    "type",
    "scroll",
    "extract",
    "back",
    "finish",
    "fail",
]


class Action(BaseModel):
    type: ActionType
    target: str | None = None
    value: str | None = None
    reason: str | None = None
