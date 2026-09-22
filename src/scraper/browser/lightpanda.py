from __future__ import annotations

from playwright.async_api import async_playwright
from ..actions import Action
from . import BrowserAdapter


class LightpandaBrowser(BrowserAdapter):
    def __init__(self, cdp_url: str) -> None:
        self._cdp_url = cdp_url
        self._playwright = None
        self._browser = None
        self._page = None

    async def connect(self) -> None:
        if not self._cdp_url:
            raise ValueError("LIGHTPANDA_CDP_URL is required")
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.connect_over_cdp(self._cdp_url)
        context = self._browser.contexts[0]
        self._page = context.pages[0] if context.pages else await context.new_page()

    async def close(self) -> None:
        if self._browser is not None:
            await self._browser.close()
        if self._playwright is not None:
            await self._playwright.stop()

    async def snapshot(self) -> str:
        if self._page is None:
            raise RuntimeError("Browser not connected")
        return await self._page.content()

    async def perform(self, action: Action) -> None:
        if self._page is None:
            raise RuntimeError("Browser not connected")
        if action.type == "navigate" and action.target:
            await self._page.goto(action.target)
            return
        if action.type == "click" and action.target:
            await self._page.locator(action.target).click()
            return
        if action.type == "type" and action.target is not None:
            await self._page.locator(action.target).fill(action.value or "")
            return
        if action.type == "scroll":
            await self._page.mouse.wheel(0, 800)
            return
        if action.type in {"finish", "fail", "extract", "back", "search"}:
            return
        raise ValueError(f"Unsupported action: {action.type}")
