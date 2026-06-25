from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SimulationReport:
    scenario: str
    final_outcome: str
    accepted: bool
    attempts: int
    failed_attempts: int
    retries_requested: int
    fallback_used: bool
    escalated: bool
    latency_ms: int
    estimated_cost_usd: float
    correctness_proxy: str
    consistency_note: str
    decision_log: list[str] = field(default_factory=list)

    @property
    def retries(self) -> int:
        """Backward-compatible alias for actual supervisor retry requests."""
        return self.retries_requested

    def to_text(self) -> str:
        lines = [
            f"Scenario: {self.scenario}",
            f"Final outcome: {self.final_outcome}",
            f"Accepted: {self.accepted}",
            f"Attempts: {self.attempts}",
            f"Failed attempts: {self.failed_attempts}",
            f"Retries requested: {self.retries_requested}",
            f"Fallback used: {self.fallback_used}",
            f"Escalated: {self.escalated}",
            f"Latency (ms): {self.latency_ms}",
            f"Estimated cost (USD): {self.estimated_cost_usd:.3f}",
            f"Correctness proxy: {self.correctness_proxy}",
            f"Consistency note: {self.consistency_note}",
            "",
            "Decision log:",
        ]
        lines.extend(f"- {item}" for item in self.decision_log)
        return "\n".join(lines)
