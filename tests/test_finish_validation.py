from scraper.state import initial_state
from scraper.validate import validate


def test_finish_fails_on_empty_results():
    state = initial_state("collect data")
    state["last_action"] = {"type": "finish"}

    updates = validate(state)

    assert updates["status"] == "failed"
    assert updates["stop_reason"] == "empty_results"


def test_finish_succeeds_with_results():
    state = initial_state("collect data")
    state["last_action"] = {"type": "finish"}
    state["results"] = [{"title": "A"}]

    updates = validate(state)

    assert updates["status"] == "completed"
