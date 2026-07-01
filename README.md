# Agent System Simulator

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/simaba/agent-simulator)](https://github.com/simaba/agent-simulator/commits/main)

A small, runnable simulator for controlled multi-agent workflows, demonstrating governance, orchestration, and evaluation through working code rather than documentation alone.

## Choose this repo when

Use this repository when you want a **concrete executable example** of:

- bounded retries
- fallback behavior
- escalation logic
- evaluator-driven acceptance
- traceable decision logs

This repo is intentionally narrower than:

- [`multi-agent-governance`](https://github.com/simaba/multi-agent-governance), which defines the governance model
- [`agent-orchestration`](https://github.com/simaba/agent-orchestration), which catalogs orchestration patterns
- [`agent-eval`](https://github.com/simaba/agent-eval), which defines broader evaluation dimensions and scenarios

## Why this exists

Agent systems are easy to describe but hard to reason about without running them. This simulator gives you a concrete, inspectable implementation of the core control patterns: explicit roles, bounded retries, fallback paths, escalation triggers, and evaluation.

The design principle is simple: a well-governed agent system should expose its control logic clearly enough to be debugged, tested, evaluated, and improved.

## How it works

```mermaid
flowchart TD
    P[Planner\nDecides how to handle the task] --> E
    E[Executor\nPerforms the task action] --> Ev
    Ev[Evaluator\nAssesses result quality] --> S
    S{Supervisor\nDecide outcome}
    S -->|Accept| Done[✓ Task complete]
    S -->|Retry| E
    S -->|Fallback| F[Fallback handler]
    S -->|Escalate| Esc[Human escalation]
```

## Agents

| Agent | Role |
|-------|------|
| **Planner** | Determines the strategy for handling the task |
| **Executor** | Performs the primary task action |
| **Evaluator** | Assesses whether the result meets acceptance criteria |
| **Supervisor** | Decides whether to accept, retry, fallback, or escalate |

## Quick start

Python 3.10 or newer is required.

### Run directly from a source checkout

The simulator uses only the Python standard library at runtime. Clone the repository and run a scenario directly:

```bash
git clone https://github.com/simaba/agent-simulator.git
cd agent-simulator
python run_demo.py --scenario normal_success
```

The `run_demo.py` wrapper adds the local `src/` directory automatically, so no manual `PYTHONPATH` setup is needed.

### Install the CLI and run tests

```bash
python -m pip install -e ".[dev]"
agent-simulator --scenario retry_then_success
python -m pytest
```

Available scenarios:

```bash
python run_demo.py --scenario normal_success
python run_demo.py --scenario retry_then_success
python run_demo.py --scenario fallback_after_failure
python run_demo.py --scenario escalate_after_failure
```

## What each run produces

- decision log with full agent interaction trace
- retry, fallback, and escalation events
- final outcome status
- scenario-configured latency and cost estimates
- evaluation summary metrics

`correctness_proxy` is a simulator-state label derived from the configured scenario outcome. It is not a measured quality, safety, or model-performance metric.

See `examples/sample-output.md` for a full example run.

## Repository structure

```text
run_demo.py             # Self-contained checkout entry point
src/
  agents.py             # Agent role implementations
  controller.py         # Orchestration and retry logic
  evaluation.py         # Evaluation report shape and rendering
  scenarios.py          # Scenario definitions
  cli.py                # Installed CLI entry point
tests/
  test_controller.py    # Scenario coverage tests
examples/
  sample-output.md      # Example run output
requirements.txt        # Runtime dependency note
pyproject.toml          # Packaging and test configuration
```

## Related repositories

| Repository | What it adds |
|---|---|
| [multi-agent-governance](https://github.com/simaba/multi-agent-governance) | Governance model for multi-agent systems |
| [agent-orchestration](https://github.com/simaba/agent-orchestration) | Broader orchestration pattern catalog |
| [agent-eval](https://github.com/simaba/agent-eval) | Evaluation framework and scenario dimensions |
| [lean-ai-ops](https://github.com/simaba/lean-ai-ops) | Another runnable repo that applies structured logic to a different domain |

---

*Shared in a personal capacity. Open to collaborations and feedback via [LinkedIn](https://linkedin.com/in/simaba) or [Medium](https://medium.com/@bagheri.sima).*