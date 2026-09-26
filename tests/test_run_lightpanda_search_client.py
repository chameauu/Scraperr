from scraper.cli import create_search_client
from scraper.search import SearxNGClient


def test_create_search_client_returns_none_when_missing():
    assert create_search_client(None) is None


def test_create_search_client_builds_client():
    client = create_search_client("http://localhost:8888")
    assert isinstance(client, SearxNGClient)
