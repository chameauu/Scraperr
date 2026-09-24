import asyncio

from scraper.actions import Action
from scraper.runner import run_agent


class FakeBrowser:
    async def snapshot(self) -> str:
        return "<html><title>Example</title><body>Hello</body></html>"

    async def perform(self, _action: Action) -> None:
        return None


async def decide(_state):
    return Action(type="finish")


async def main():
    result = await run_agent("collect data", browser=FakeBrowser(), decide=decide)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
