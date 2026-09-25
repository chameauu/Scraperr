from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from bs4 import BeautifulSoup


@dataclass(frozen=True)
class CompactObservation:
    title: str | None
    links: list[str]
    buttons: list[str]
    inputs: list[str]
    text_snippet: str


def _unique(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            output.append(value)
    return output


def build_compact_observation(html: str, *, max_text: int = 2000) -> CompactObservation:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else None

    links = _unique([a.get_text(strip=True) for a in soup.find_all("a")])
    button_labels = [b.get_text(strip=True) for b in soup.find_all("button")]
    input_buttons = [
        (i.get("value") or "").strip()
        for i in soup.find_all("input")
        if (i.get("type") or "").lower() in {"button", "submit"}
    ]
    buttons = _unique(button_labels + input_buttons)
    inputs = _unique(
        [i.get("name") or i.get("id") or "" for i in soup.find_all(["input", "textarea", "select"])]
    )

    text = " ".join(soup.stripped_strings)
    if len(text) > max_text:
        text = text[:max_text]

    return CompactObservation(
        title=title,
        links=links,
        buttons=buttons,
        inputs=inputs,
        text_snippet=text,
    )
