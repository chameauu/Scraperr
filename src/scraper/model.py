from __future__ import annotations

from typing import Protocol

from .actions import Action
from .state import GraphState


class ModelClient(Protocol):
    async def decide_action(self, state: GraphState) -> Action: ...

    async def generate_schema(self, state: GraphState) -> dict: ...

    async def extract_data(self, state: GraphState) -> list[dict]: ...
