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
    progress=None,
) -> AsyncIterator[None]:
    try:
        if hasattr(browser, "connect"):
            if progress is not None:
                await progress({"kind": "runtime_connect_start"})
            await browser.connect()
            if progress is not None:
                await progress({"kind": "runtime_connect_done"})
        yield
    finally:
        if search_client is not None:
            await search_client.aclose()
        if model is not None and hasattr(model, "aclose"):
            await model.aclose()
        if hasattr(browser, "close"):
            if progress is not None:
                await progress({"kind": "runtime_close_start"})
            await browser.close()
            if progress is not None:
                await progress({"kind": "runtime_close_done"})
