#!/usr/bin/env python3
"""Validate AGENTS.md / CLAUDE.md pointer-doc invariants."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PATH_PATTERN = re.compile(r"(?<!https://)(?<!http://)(?<!file://)\b(?:\.?\.?/)?[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+\.[A-Za-z0-9]+")


def extract_repo_paths(text: str) -> set[str]:
    matches = set(PATH_PATTERN.findall(text))
    filtered: set[str] = set()
    for match in matches:
        if match.startswith("/"):
            continue
        if match.startswith("output/"):
            continue
        filtered.add(match)
    return filtered


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    agents = root / "AGENTS.md"
    claude = root / "CLAUDE.md"

    if not agents.exists():
        errors.append("AGENTS.md is missing")
        return errors
    if not claude.exists():
        errors.append("CLAUDE.md is missing")
        return errors

    agents_text = agents.read_text(encoding="utf-8")
    claude_text = claude.read_text(encoding="utf-8")

    if agents_text != claude_text:
        errors.append("AGENTS.md and CLAUDE.md differ")

    line_count = len(agents_text.splitlines())
    if line_count > 90:
        errors.append(f"Pointer docs should stay <= 90 lines (got {line_count})")

    for rel_path in sorted(extract_repo_paths(agents_text)):
        path = root / rel_path
        if not path.exists():
            errors.append(f"Pointer path does not exist: {rel_path}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate root pointer docs.")
    parser.add_argument("--root", default=".", help="Repository root (default: current directory)")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Pointer docs valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
