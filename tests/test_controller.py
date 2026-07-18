from __future__ import annotations

import pytest

from agents import EvaluatorAgent, ExecutorResult
from controller import run_scenario


REQUIRED = ("task_complete", "output_present", "boundary_respected")


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
    assert any("not used as authorization" in item for item in report.decision_log)


def test_retry_then_success_path_uses_evidence_not_confidence() -> None:
    report = run_scenario("retry_then_success")

    assert report.accepted is True
    assert report.attempts == 2
    assert report.failed_attempts == 1
    assert report.retries_requested == 1
    assert report.fallback_used is False
    assert report.escalated is False
    assert any("task_complete" in item for item in report.decision_log)
    assert any("self_reported_confidence=0.91" in item for item in report.decision_log)
    assert any("self_reported_confidence=0.72" in item for item in report.decision_log)
    assert any("bounded retry" in item.lower() for item in report.decision_log)


def test_high_confidence_does_not_override_missing_evidence() -> None:
    execution = ExecutorResult(
        output="Confident but incomplete result.",
        evidence={
            "task_complete": False,
            "output_present": True,
            "boundary_respected": True,
        },
        reported_confidence=0.99,
    )

    review = EvaluatorAgent().act(execution, REQUIRED)

    assert review.accepted is False
    assert review.failed_criteria == ["task_complete"]


def test_lower_confidence_does_not_block_demonstrated_criteria() -> None:
    execution = ExecutorResult(
        output="Complete bounded result.",
        evidence={
            "task_complete": True,
            "output_present": True,
            "boundary_respected": True,
        },
        reported_confidence=0.41,
    )

    review = EvaluatorAgent().act(execution, REQUIRED)

    assert review.accepted is True
    assert review.failed_criteria == []


def test_fallback_after_failure_validates_separate_fallback_contract() -> None:
    report = run_scenario("fallback_after_failure")

    assert report.accepted is False
    assert report.attempts == 2
    assert report.failed_attempts == 2
    assert report.retries_requested == 1
    assert report.fallback_used is True
    assert report.escalated is False
    assert report.final_outcome.startswith("Fallback path used")
    assert any("evaluated fallback contract" in item.lower() for item in report.decision_log)
    assert any("validated fallback path" in item.lower() for item in report.decision_log)


def test_escalate_after_failure_path_is_runnable_and_traceable() -> None:
    report = run_scenario("escalate_after_failure")

    assert report.accepted is False
    assert report.attempts == 2
    assert report.failed_attempts == 2
    assert report.retries_requested == 1
    assert report.fallback_used is False
    assert report.escalated is True
    assert report.final_outcome == "Escalated to human review."
    assert any("boundary_respected" in item for item in report.decision_log)
    assert any("escalated to human review" in item.lower() for item in report.decision_log)


def test_unknown_scenario_fails_with_available_choices() -> None:
    with pytest.raises(ValueError, match="Available scenarios"):
        run_scenario("does_not_exist")
