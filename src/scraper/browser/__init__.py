from __future__ import annotations

from typing import Protocol
from ..actions import Action


class BrowserAdapter(Protocol):
    async def snapshot(self) -> str: ...

    async def perform(self, action: Action) -> None: ...
