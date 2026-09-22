from __future__ import annotations

from typing import Literal, Optional
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
    target: Optional[str] = None
    value: Optional[str] = None
    reason: Optional[str] = None
