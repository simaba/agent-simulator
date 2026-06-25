from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PlannerResult:
    plan: str


@dataclass
class ExecutorResult:
    output: str
    confidence: float
    success: bool


@dataclass
class EvaluatorResult:
    accepted: bool
    reason: str


class PlannerAgent:
    def act(self, task: str) -> PlannerResult:
        return PlannerResult(plan=f"Handle task with bounded workflow: {task}")


class ExecutorAgent:
    def act(self, scenario_name: str, attempt: int) -> ExecutorResult:
        if scenario_name == "normal_success":
            return ExecutorResult(output="Completed successfully on first pass.", confidence=0.93, success=True)
        if scenario_name == "retry_then_success":
            if attempt == 1:
                return ExecutorResult(output="Initial result is incomplete.", confidence=0.49, success=False)
            return ExecutorResult(output="Improved result accepted after retry.", confidence=0.85, success=True)
        if scenario_name == "fallback_after_failure":
            return ExecutorResult(output="Primary path failed to produce an acceptable result.", confidence=0.31, success=False)
        if scenario_name == "escalate_after_failure":
            return ExecutorResult(output="High-impact primary path failed validation.", confidence=0.20, success=False)
        return ExecutorResult(output="Unknown scenario.", confidence=0.0, success=False)


class EvaluatorAgent:
    def act(self, execution: ExecutorResult) -> EvaluatorResult:
        if execution.success and execution.confidence >= 0.8:
            return EvaluatorResult(accepted=True, reason="Output meets acceptance threshold.")
        if execution.confidence < 0.5:
            return EvaluatorResult(accepted=False, reason="Confidence below acceptance threshold.")
        return EvaluatorResult(accepted=False, reason="Output not sufficiently reliable.")
