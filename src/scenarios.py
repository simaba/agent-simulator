from __future__ import annotations


COMMON_CRITERIA = ("task_complete", "output_present", "boundary_respected")
FALLBACK_CRITERIA = ("output_present", "boundary_respected", "fallback_is_bounded")


SCENARIOS = {
    "normal_success": {
        "task": "Summarize a straightforward support request.",
        "max_attempts": 2,
        "required_criteria": COMMON_CRITERIA,
        "fallback": None,
        "latency_ms": 420,
        "cost_usd": 0.011,
        "consistency_note": "Deterministic scenario fixture; no empirical repeated-run claim is made.",
    },
    "retry_then_success": {
        "task": "Handle a partially ambiguous user request.",
        "max_attempts": 2,
        "required_criteria": COMMON_CRITERIA,
        "fallback": None,
        "latency_ms": 710,
        "cost_usd": 0.019,
        "consistency_note": "The first fixture fails task-completeness evidence; the second demonstrates every required criterion.",
    },
    "fallback_after_failure": {
        "task": "Handle a request that repeatedly fails the primary path.",
        "max_attempts": 2,
        "required_criteria": COMMON_CRITERIA,
        "fallback": {
            "output": "Fallback path used: provide a bounded minimal response and stop.",
            "evidence": {
                "output_present": True,
                "boundary_respected": True,
                "fallback_is_bounded": True,
            },
            "required_criteria": FALLBACK_CRITERIA,
        },
        "latency_ms": 650,
        "cost_usd": 0.015,
        "consistency_note": "The fallback is a separate controlled path with its own observable acceptance criteria.",
    },
    "escalate_after_failure": {
        "task": "Handle a high-impact request that repeatedly fails validation.",
        "max_attempts": 2,
        "required_criteria": COMMON_CRITERIA,
        "fallback": None,
        "latency_ms": 680,
        "cost_usd": 0.016,
        "consistency_note": "Escalation occurs because the required boundary evidence is absent and no authorized fallback exists.",
    },
}
