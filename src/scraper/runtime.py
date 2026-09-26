from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from .browser import BrowserAdapter
from .model import ModelClient
from .search import SearxNGClient


@asynccontextmanager
async def agent_runtime(
    *,
    browser: BrowserAdapter,
    model: ModelClient | None = None,
    search_client: SearxNGClient | None = None,
) -> AsyncIterator[None]:
    try:
        if hasattr(browser, "connect"):
            await browser.connect()
        yield
    finally:
        if search_client is not None:
            await search_client.aclose()
        if model is not None and hasattr(model, "aclose"):
            await model.aclose()
        if hasattr(browser, "close"):
            await browser.close()
