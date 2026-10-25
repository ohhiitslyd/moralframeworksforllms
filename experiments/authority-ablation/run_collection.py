"""Shim so the collection can be launched under tools/run_reserved.py (which runs a script path, not -m).

    python -u tools/run_reserved.py experiments/authority-ablation/run_collection.py <lying_harness.pressure args>

Identical to `python -u -m lying_harness.pressure <args>`; it only adds the worktree root to sys.path.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lying_harness.pressure import main  # noqa: E402

if __name__ == "__main__":
    main()
