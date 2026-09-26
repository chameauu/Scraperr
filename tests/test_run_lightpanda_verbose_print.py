from scraper.cli import format_progress_event


def test_format_progress_event_includes_kind():
    event = {"kind": "pre_execute", "action": {"type": "navigate"}}
    output = format_progress_event(event)
    assert "pre_execute" in output
