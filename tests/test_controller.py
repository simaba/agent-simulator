from __future__ import annotations

import pytest

from controller import run_scenario


def test_normal_success_path() -> None:
    report = run_scenario("normal_success")

    assert report.accepted is True
    assert report.attempts == 1
    assert report.failed_attempts == 0
    assert report.retries_requested == 0
    assert report.retries == 0
    assert report.fallback_used is False
    assert report.escalated is False
    assert "Planner created plan" in report.decision_log[0]


def test_retry_then_success_path_counts_only_requested_retries() -> None:
    report = run_scenario("retry_then_success")

    assert report.accepted is True
    assert report.attempts == 2
    assert report.failed_attempts == 1
    assert report.retries_requested == 1
    assert report.fallback_used is False
    assert report.escalated is False
    assert any("bounded retry" in item.lower() for item in report.decision_log)


def test_fallback_after_failure_does_not_count_terminal_failure_as_retry() -> None:
    report = run_scenario("fallback_after_failure")

    assert report.accepted is False
    assert report.attempts == 2
    assert report.failed_attempts == 2
    assert report.retries_requested == 1
    assert report.fallback_used is True
    assert report.escalated is False
    assert report.final_outcome.startswith("Fallback path used")
    assert any("fallback path" in item.lower() for item in report.decision_log)


def test_escalate_after_failure_path_is_runnable_and_traceable() -> None:
    report = run_scenario("escalate_after_failure")

    assert report.accepted is False
    assert report.attempts == 2
    assert report.failed_attempts == 2
    assert report.retries_requested == 1
    assert report.fallback_used is False
    assert report.escalated is True
    assert report.final_outcome == "Escalated to human review."
    assert any("escalated to human review" in item.lower() for item in report.decision_log)


def test_unknown_scenario_fails_with_available_choices() -> None:
    with pytest.raises(ValueError, match="Available scenarios"):
        run_scenario("does_not_exist")
