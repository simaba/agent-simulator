from __future__ import annotations

from src.agents import EvaluatorAgent, ExecutorAgent, PlannerAgent
from src.evaluation import SimulationReport
from src.scenarios import SCENARIOS


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
        decision_log.append(
            f"Executor attempt {attempt}: success={execution.success}, confidence={execution.confidence:.2f}"
        )
        review = evaluator.act(execution)
        decision_log.append(f"Evaluator decision: accepted={review.accepted}, reason={review.reason}")

        if review.accepted:
            accepted = True
            final_outcome = execution.output
            break

        failed_attempts += 1
        if attempt >= scenario["max_attempts"]:
            if scenario["use_fallback"]:
                fallback_used = True
                final_outcome = scenario["fallback_output"]
                decision_log.append("Supervisor triggered fallback path.")
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
