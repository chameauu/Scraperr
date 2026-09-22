from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    cdp_url: str
    max_steps: int = 20
    max_retries: int = 2


    @staticmethod
    def from_env() -> "Settings":
        return Settings(
            cdp_url=os.getenv("LIGHTPANDA_CDP_URL", ""),
            max_steps=int(os.getenv("SCRAPER_MAX_STEPS", "20")),
            max_retries=int(os.getenv("SCRAPER_MAX_RETRIES", "2")),
        )
