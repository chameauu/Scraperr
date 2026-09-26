from __future__ import annotations

import argparse

from .search import SearxNGClient


def build_lightpanda_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Lightpanda scraping agent")
    parser.add_argument("--task", help="Scraping objective", default=None)
    parser.add_argument("--start-url", help="Optional start URL", default=None)
    parser.add_argument("--verbose", help="Print progress events", action="store_true")
    return parser.parse_args(argv)


def create_search_client(base_url: str | None) -> SearxNGClient | None:
    if not base_url:
        return None
    return SearxNGClient(base_url=base_url)


def format_progress_event(event: dict) -> str:
    kind = event.get("kind", "event")
    return f"[{kind}] {event}"
