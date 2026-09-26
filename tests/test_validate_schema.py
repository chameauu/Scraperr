from scraper.state import initial_state
from scraper.validate import validate


def test_finish_fails_when_schema_missing():
    state = initial_state("collect data")
    state["last_action"] = {"type": "finish"}
    state["results"] = [{"title": "A"}]

    updates = validate(state)

    assert updates["status"] == "failed"
    assert updates["stop_reason"] == "missing_schema"
