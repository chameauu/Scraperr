from scraper.cli import build_lightpanda_args


def test_build_args_defaults():
    args = build_lightpanda_args([])
    assert args.task is None
    assert args.start_url is None


def test_build_args_parses_values():
    args = build_lightpanda_args(["--task", "collect", "--start-url", "https://example.com"])
    assert args.task == "collect"
    assert args.start_url == "https://example.com"
