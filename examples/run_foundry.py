import asyncio
import os

from dotenv import load_dotenv

from scraper.actions import Action
from scraper.foundry_responses import FoundryResponsesModel
from scraper.runner import run_agent
from scraper.search import SearxNGClient


class FakeBrowser:
    async def snapshot(self) -> str:
        return "<html><title>Example</title><body>Hello</body></html>"

    async def perform(self, _action: Action) -> None:
        return None


async def main() -> None:
    load_dotenv()
    endpoint = os.environ["FOUNDRY_ENDPOINT"]
    api_key = os.environ["FOUNDRY_API_KEY"]
    model = os.environ["FOUNDRY_MODEL"]
    searxng_base_url = os.environ["SEARXNG_BASE_URL"]

    client = FoundryResponsesModel(endpoint=endpoint, api_key=api_key, model=model)
    search_client = SearxNGClient(base_url=searxng_base_url)
    result = await run_agent(
        "give me latest 10 news on hackernews",
        browser=FakeBrowser(),
        model=client,
        search_client=search_client,
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
