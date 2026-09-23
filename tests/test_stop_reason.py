from scraper.state import initial_state
from scraper.validate import validate


def test_stop_reason_on_retry_exhaustion():
    state = initial_state("collect data", max_retries=0)
    state["last_error"] = "boom"

    updates = validate(state)

    assert updates["status"] == "failed"
    assert updates["stop_reason"] == "retries_exhausted"


def test_stop_reason_on_max_steps():
    state = initial_state("collect data", max_steps=1)
    state["step"] = 1

    updates = validate(state)

    assert updates["status"] == "failed"
    assert updates["stop_reason"] == "max_steps_reached"
