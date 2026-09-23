from scraper.safety import is_safe_url


def test_is_safe_url_rejects_localhost():
    assert is_safe_url("http://localhost:8000") is False
    assert is_safe_url("http://127.0.0.1") is False
    assert is_safe_url("http://[::1]") is False


def test_is_safe_url_rejects_private_ip():
    assert is_safe_url("http://192.168.1.10") is False
    assert is_safe_url("http://10.0.0.5") is False
    assert is_safe_url("http://172.16.0.1") is False


def test_is_safe_url_allows_public_http():
    assert is_safe_url("https://example.com") is True
    assert is_safe_url("http://example.com/path") is True
