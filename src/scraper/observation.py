from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from bs4 import BeautifulSoup


@dataclass(frozen=True)
class CompactObservation:
    title: str | None
    links: list[dict]
    buttons: list[dict]
    inputs: list[dict]
    text_snippet: str


def _unique(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            output.append(value)
    return output


def _css_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _build_selector(tag: str, attrs: dict) -> str | None:
    element_id = (attrs.get("id") or "").strip()
    if element_id:
        return f"{tag}#{element_id}"
    data_testid = (attrs.get("data-testid") or "").strip()
    if data_testid:
        return f'{tag}[data-testid="{_css_escape(data_testid)}"]'
    aria_label = (attrs.get("aria-label") or "").strip()
    if aria_label:
        return f'{tag}[aria-label="{_css_escape(aria_label)}"]'
    name = (attrs.get("name") or "").strip()
    if name:
        return f'{tag}[name="{_css_escape(name)}"]'
    href = (attrs.get("href") or "").strip()
    if href and tag == "a":
        return f'{tag}[href="{_css_escape(href)}"]'
    return None


def build_compact_observation(html: str, *, max_text: int = 2000) -> CompactObservation:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else None

    links: list[dict] = []
    for link in soup.find_all("a"):
        label = link.get_text(strip=True)
        selector = _build_selector("a", link.attrs)
        href = link.get("href")
        if label or selector or href:
            links.append({"label": label, "selector": selector, "href": href})

    buttons: list[dict] = []
    for button in soup.find_all("button"):
        label = button.get_text(strip=True)
        selector = _build_selector("button", button.attrs)
        if label or selector:
            buttons.append({"label": label, "selector": selector})

    for input_el in soup.find_all("input"):
        input_type = (input_el.get("type") or "").lower()
        if input_type in {"button", "submit"}:
            label = (input_el.get("value") or "").strip()
            selector = _build_selector("input", input_el.attrs)
            if label or selector:
                buttons.append({"label": label, "selector": selector})

    inputs: list[dict] = []
    for input_el in soup.find_all(["input", "textarea", "select"]):
        name = (input_el.get("name") or "").strip()
        element_id = (input_el.get("id") or "").strip()
        selector = _build_selector(input_el.name, input_el.attrs)
        if name or element_id or selector:
            inputs.append({"name": name or element_id, "selector": selector})

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
