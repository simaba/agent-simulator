from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PlannerResult:
    plan: str


@dataclass
class ExecutorResult:
    output: str
    evidence: dict[str, bool]
    reported_confidence: float


@dataclass
class EvaluatorResult:
    accepted: bool
    reason: str
    failed_criteria: list[str] = field(default_factory=list)


class PlannerAgent:
    def act(self, task: str) -> PlannerResult:
        return PlannerResult(plan=f"Handle task with bounded workflow: {task}")


class ExecutorAgent:
    def act(self, scenario_name: str, attempt: int) -> ExecutorResult:
        if scenario_name == "normal_success":
            return ExecutorResult(
                output="Completed successfully on first pass.",
                evidence={
                    "task_complete": True,
                    "output_present": True,
                    "boundary_respected": True,
                },
                reported_confidence=0.93,
            )
        if scenario_name == "retry_then_success":
            if attempt == 1:
                return ExecutorResult(
                    output="Initial result is incomplete.",
                    evidence={
                        "task_complete": False,
                        "output_present": True,
                        "boundary_respected": True,
                    },
                    reported_confidence=0.91,
                )
            return ExecutorResult(
                output="Improved result accepted after retry.",
                evidence={
                    "task_complete": True,
                    "output_present": True,
                    "boundary_respected": True,
                },
                reported_confidence=0.72,
            )
        if scenario_name == "fallback_after_failure":
            return ExecutorResult(
                output="Primary path failed to produce a complete result.",
                evidence={
                    "task_complete": False,
                    "output_present": True,
                    "boundary_respected": True,
                },
                reported_confidence=0.88,
            )
        if scenario_name == "escalate_after_failure":
            return ExecutorResult(
                output="High-impact path could not demonstrate the required boundary control.",
                evidence={
                    "task_complete": False,
                    "output_present": True,
                    "boundary_respected": False,
                },
                reported_confidence=0.95,
            )
        return ExecutorResult(
            output="Unknown scenario.",
            evidence={
                "task_complete": False,
                "output_present": False,
                "boundary_respected": False,
            },
            reported_confidence=0.0,
        )


class EvaluatorAgent:
    def act(
        self,
        execution: ExecutorResult,
        required_criteria: tuple[str, ...],
    ) -> EvaluatorResult:
        failed = [
            criterion
            for criterion in required_criteria
            if execution.evidence.get(criterion) is not True
        ]
        if failed:
            return EvaluatorResult(
                accepted=False,
                reason="Required observable criteria were not demonstrated: "
                + ", ".join(failed),
                failed_criteria=failed,
            )
        return EvaluatorResult(
            accepted=True,
            reason="All required observable criteria were demonstrated.",
        )
