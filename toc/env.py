from __future__ import annotations

import os
from pathlib import Path


def _strip_quotes(value: str) -> str:
    v = value.strip()
    if len(v) >= 2 and ((v[0] == v[-1] == '"') or (v[0] == v[-1] == "'")):
        return v[1:-1]
    return v


def load_env_file(path: Path, *, override: bool = False) -> None:
    """
    Minimal .env loader (key=value).

    - Ignores blank lines and comments (# ...)
    - Supports optional "export KEY=value"
    - Does not override existing os.environ unless override=True
    """
    if not path.exists() or not path.is_file():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            continue
        value = _strip_quotes(value)

        if not override and key in os.environ:
            continue
        os.environ[key] = value


def load_env_files(
    *,
    repo_root: Path | None = None,
    filenames: tuple[str, ...] = (".env", ".env.local"),
    override: bool = False,
) -> None:
    """
    Load env vars from (repo_root / filename) in order.
    Later files can override earlier ones if override=True.
    """
    base = repo_root or Path.cwd()
    for name in filenames:
        load_env_file(base / name, override=override)

