import asyncio
import os

from dotenv import load_dotenv

from scraper.browser.lightpanda import LightpandaBrowser
from scraper.cli import build_lightpanda_args, create_search_client, format_progress_event
from scraper.foundry_responses import FoundryResponsesModel
from scraper.runner import run_agent


async def main() -> None:
    load_dotenv()
    args = build_lightpanda_args()
    print({"kind": "startup", "message": "starting lightpanda run"}, flush=True)
    cdp_url = os.environ["LIGHTPANDA_CDP_URL"]
    endpoint = os.environ["FOUNDRY_ENDPOINT"]
    api_key = os.environ["FOUNDRY_API_KEY"]
    model = os.environ["FOUNDRY_MODEL"]
    searxng_base_url = os.environ.get("SEARXNG_BASE_URL")
    task = args.task or os.environ.get("SCRAPER_TASK", "get latest 10 hackernews articles")
    nav_timeout_ms = int(os.environ.get("LIGHTPANDA_NAV_TIMEOUT_MS", "30000"))
    snapshot_timeout_s = float(os.environ.get("LIGHTPANDA_SNAPSHOT_TIMEOUT_S", "30"))

    browser = LightpandaBrowser(cdp_url=cdp_url, navigation_timeout_ms=nav_timeout_ms)
    client = FoundryResponsesModel(endpoint=endpoint, api_key=api_key, model=model)
    search_client = create_search_client(searxng_base_url)

    async def progress(event: dict) -> None:
        if args.verbose:
            print(format_progress_event(event), flush=True)

    print({"kind": "connect", "message": "connecting to lightpanda"}, flush=True)
    result = await run_agent(
        task,
        browser=browser,
        model=client,
        search_client=search_client,
        decide=None,
        progress=progress,
        observe_timeout_s=snapshot_timeout_s,
    )
    if args.verbose:
        print(
            format_progress_event(
                {
                    "kind": "final",
                    "status": result.get("status"),
                    "stop_reason": result.get("stop_reason"),
                }
            ),
            flush=True,
        )
    print(result, flush=True)


if __name__ == "__main__":
    asyncio.run(main())
