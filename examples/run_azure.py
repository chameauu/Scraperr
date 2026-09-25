import asyncio
import os

from dotenv import load_dotenv

from scraper.actions import Action
from scraper.azure_openai import AzureOpenAIModel
from scraper.runner import run_agent


class FakeBrowser:
    async def snapshot(self) -> str:
        return "<html><title>Example</title><body>Hello</body></html>"

    async def perform(self, _action: Action) -> None:
        return None


async def main() -> None:
    load_dotenv()
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    api_key = os.environ["AZURE_OPENAI_API_KEY"]
    deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]
    api_version = os.environ["AZURE_OPENAI_API_VERSION"]

    model = AzureOpenAIModel(
        endpoint=endpoint,
        api_key=api_key,
        deployment=deployment,
        api_version=api_version,
    )

    result = await run_agent("collect data", browser=FakeBrowser(), model=model)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
