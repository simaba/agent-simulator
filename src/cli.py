from __future__ import annotations

import argparse

from controller import run_scenario
from scenarios import SCENARIOS


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a small multi-agent system simulation."
    )
    parser.add_argument(
        "--scenario",
        choices=sorted(SCENARIOS),
        default="normal_success",
        help="Scenario to simulate",
    )
    args = parser.parse_args()

    report = run_scenario(args.scenario)
    print(report.to_text())


if __name__ == "__main__":
    main()
