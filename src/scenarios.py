from __future__ import annotations


SCENARIOS = {
    "normal_success": {
        "task": "Summarize a straightforward support request.",
        "max_attempts": 2,
        "use_fallback": False,
        "fallback_output": "",
        "latency_ms": 420,
        "cost_usd": 0.011,
        "consistency_note": "Stable across repeated runs in this simple path.",
    },
    "retry_then_success": {
        "task": "Handle a partially ambiguous user request.",
        "max_attempts": 2,
        "use_fallback": False,
        "fallback_output": "",
        "latency_ms": 710,
        "cost_usd": 0.019,
        "consistency_note": "Moderately stable but sensitive to evaluator thresholds.",
    },
    "fallback_after_failure": {
        "task": "Handle a request that repeatedly fails the primary path.",
        "max_attempts": 2,
        "use_fallback": True,
        "fallback_output": "Fallback path used: produce a safe minimal response.",
        "latency_ms": 650,
        "cost_usd": 0.015,
        "consistency_note": "Stable once fallback is triggered, but quality is intentionally reduced.",
    },
    "escalate_after_failure": {
        "task": "Handle a high-impact request that repeatedly fails validation.",
        "max_attempts": 2,
        "use_fallback": False,
        "fallback_output": "",
        "latency_ms": 680,
        "cost_usd": 0.016,
        "consistency_note": "Human escalation is required when bounded recovery paths do not produce an acceptable result.",
    },
}
