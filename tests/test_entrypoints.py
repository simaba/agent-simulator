from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def test_checkout_demo_entry_point_runs_without_pythonpath() -> None:
    result = subprocess.run(
        [sys.executable, "run_demo.py", "--scenario", "normal_success"],
        cwd=REPOSITORY_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Scenario: normal_success" in result.stdout
