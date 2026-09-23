from __future__ import annotations

from ipaddress import ip_address
from urllib.parse import urlparse


def is_safe_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return False

    host = parsed.hostname
    if host is None:
        return False

    lower_host = host.lower()
    if lower_host in {"localhost", "127.0.0.1", "::1"}:
        return False
    if lower_host.endswith(".localhost"):
        return False

    try:
        ip = ip_address(lower_host)
    except ValueError:
        return True

    return not (ip.is_loopback or ip.is_private or ip.is_link_local)
