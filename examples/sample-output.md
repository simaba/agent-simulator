# Sample Output

Example run:

```text
Scenario: retry_then_success
Final outcome: Improved result accepted after retry.
Accepted: True
Attempts: 2
Failed attempts: 1
Retries requested: 1
Fallback used: False
Escalated: False
Latency (ms): 710
Estimated cost (USD): 0.019
Correctness proxy: high
Consistency note: The first fixture fails task-completeness evidence; the second demonstrates every required criterion.

Decision log:
- Planner created plan: Handle task with bounded workflow: Handle a partially ambiguous user request.
- Executor attempt 1: evidence[boundary_respected=True, output_present=True, task_complete=False], self_reported_confidence=0.91 (recorded, not used as authorization)
- Evaluator decision: accepted=False, reason=Required observable criteria were not demonstrated: task_complete
- Supervisor requested bounded retry.
- Executor attempt 2: evidence[boundary_respected=True, output_present=True, task_complete=True], self_reported_confidence=0.72 (recorded, not used as authorization)
- Evaluator decision: accepted=True, reason=All required observable criteria were demonstrated.
```

The first attempt deliberately reports higher confidence than the accepted second attempt. Acceptance follows the observable scenario contract, not the executor's self-assessment.
