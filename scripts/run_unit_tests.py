#!/usr/bin/env python3
"""
Run unit tests without hitting paid APIs.

This runner stops early after N failures/errors to reduce iteration cost.

Usage:
  python scripts/run_unit_tests.py            # default max failures = 3
  python scripts/run_unit_tests.py --max-failures 3
"""

from __future__ import annotations

import argparse
import sys
import unittest
from pathlib import Path


class StopAfterFailuresResult(unittest.TextTestResult):
    def __init__(self, *args, max_failures: int = 3, **kwargs):  # noqa: ANN002, ANN003
        super().__init__(*args, **kwargs)
        self._max_failures = int(max_failures)

    def _maybe_stop(self) -> None:
        if self._max_failures <= 0:
            return
        if (len(self.failures) + len(self.errors)) >= self._max_failures:
            self.shouldStop = True

    def addFailure(self, test, err):  # noqa: N802, ANN001
        super().addFailure(test, err)
        self._maybe_stop()

    def addError(self, test, err):  # noqa: N802, ANN001
        super().addError(test, err)
        self._maybe_stop()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run unit tests (stop after N failures).")
    parser.add_argument("--max-failures", type=int, default=3)
    parser.add_argument("--start-dir", default="tests")
    parser.add_argument("--pattern", default="test*.py")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root))

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=args.start_dir, pattern=args.pattern)

    runner = unittest.TextTestRunner(
        verbosity=2,
        resultclass=lambda *a, **k: StopAfterFailuresResult(*a, max_failures=args.max_failures, **k),
    )
    result = runner.run(suite)

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
