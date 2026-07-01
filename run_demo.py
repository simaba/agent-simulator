"""Run the simulator directly from a source checkout.

For an installed package, prefer the ``agent-simulator`` command. This small
wrapper keeps the documented checkout demo usable without requiring callers to
manually set ``PYTHONPATH``.
"""

from __future__ import annotations

import sys
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from cli import main  # noqa: E402


if __name__ == "__main__":
    main()
