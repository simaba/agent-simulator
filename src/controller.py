from __future__ import annotations

from agents import EvaluatorAgent, ExecutorAgent, ExecutorResult, PlannerAgent
from evaluation import SimulationReport
from scenarios import SCENARIOS


def run_scenario(name: str) -> SimulationReport:
    if name not in SCENARIOS:
        available = ", ".join(sorted(SCENARIOS))
        raise ValueError(f"Unknown scenario: {name}. Available scenarios: {available}")

    scenario = SCENARIOS[name]
    planner = PlannerAgent()
    executor = ExecutorAgent()
    evaluator = EvaluatorAgent()

    decision_log: list[str] = []
    attempts = 0
    failed_attempts = 0
    retries_requested = 0
    fallback_used = False
    escalated = False

    plan = planner.act(scenario["task"])
    decision_log.append(f"Planner created plan: {plan.plan}")

    accepted = False
    final_outcome = ""

    for attempt in range(1, scenario["max_attempts"] + 1):
        attempts = attempt
        execution = executor.act(name, attempt)
        evidence_summary = ", ".join(
            f"{key}={value}" for key, value in sorted(execution.evidence.items())
        )
        decision_log.append(
            f"Executor attempt {attempt}: evidence[{evidence_summary}], "
            f"self_reported_confidence={execution.reported_confidence:.2f} "
            "(recorded, not used as authorization)"
        )
        review = evaluator.act(execution, scenario["required_criteria"])
        decision_log.append(
            f"Evaluator decision: accepted={review.accepted}, reason={review.reason}"
        )

        if review.accepted:
            accepted = True
            final_outcome = execution.output
            break

        failed_attempts += 1
        if attempt >= scenario["max_attempts"]:
            fallback_config = scenario.get("fallback")
            if fallback_config:
                fallback_execution = ExecutorResult(
                    output=fallback_config["output"],
                    evidence=dict(fallback_config["evidence"]),
                    reported_confidence=0.0,
                )
                fallback_review = evaluator.act(
                    fallback_execution,
                    fallback_config["required_criteria"],
                )
                decision_log.append(
                    "Supervisor evaluated fallback contract: "
                    f"accepted={fallback_review.accepted}, reason={fallback_review.reason}"
                )
                if fallback_review.accepted:
                    fallback_used = True
                    final_outcome = fallback_execution.output
                    decision_log.append("Supervisor triggered the validated fallback path.")
                else:
                    escalated = True
                    final_outcome = "Escalated to human review."
                    decision_log.append(
                        "Fallback failed its own acceptance contract; supervisor escalated."
                    )
            else:
                escalated = True
                final_outcome = "Escalated to human review."
                decision_log.append("Supervisor escalated to human review.")
            break

        retries_requested += 1
        decision_log.append("Supervisor requested bounded retry.")

    correctness_proxy = "high" if accepted else ("medium" if fallback_used else "low")
    return SimulationReport(
        scenario=name,
        final_outcome=final_outcome,
        accepted=accepted,
        attempts=attempts,
        failed_attempts=failed_attempts,
        retries_requested=retries_requested,
        fallback_used=fallback_used,
        escalated=escalated,
        latency_ms=scenario["latency_ms"],
        estimated_cost_usd=scenario["cost_usd"],
        correctness_proxy=correctness_proxy,
        consistency_note=scenario["consistency_note"],
        decision_log=decision_log,
    )
