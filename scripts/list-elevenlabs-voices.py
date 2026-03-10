#!/usr/bin/env python3
"""
List available ElevenLabs voices for the configured API key.

Uses the same env loading as other scripts (reads .env via toc.env.load_env_files).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toc.env import load_env_files
from toc.http import HttpError, request_bytes


def _env(name: str, default: str | None = None) -> str | None:
    v = os.environ.get(name)
    if v is None or v == "":
        return default
    return v


def main() -> None:
    load_env_files(repo_root=REPO_ROOT)

    parser = argparse.ArgumentParser(description="List ElevenLabs voices.")
    parser.add_argument("--api-key", default=_env("ELEVENLABS_API_KEY"))
    parser.add_argument("--api-base", default=_env("ELEVENLABS_API_BASE", "https://api.elevenlabs.io/v1"))
    args = parser.parse_args()

    if not args.api_key:
        raise SystemExit("Missing ELEVENLABS_API_KEY")

    base = str(args.api_base).rstrip("/")
    url = f"{base}/voices"
    try:
        raw = request_bytes(url=url, method="GET", headers={"xi-api-key": str(args.api_key)})
    except HttpError as e:
        raise SystemExit(str(e)) from e

    data = json.loads(raw.decode("utf-8"))
    voices = data.get("voices") if isinstance(data, dict) else None
    if not isinstance(voices, list):
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    for v in voices:
        if not isinstance(v, dict):
            continue
        voice_id = v.get("voice_id")
        name = v.get("name")
        category = v.get("category")
        fine_tuning = v.get("fine_tuning") if isinstance(v.get("fine_tuning"), dict) else {}
        is_allowed = fine_tuning.get("is_allowed_to_fine_tune") if isinstance(fine_tuning, dict) else None
        print(f"{voice_id}\t{category}\t{name}\tallowed_to_finetune={is_allowed}")


if __name__ == "__main__":
    main()
