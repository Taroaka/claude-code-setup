#!/usr/bin/env python3
"""
Cheap voice_id check without generating audio.

This uses the ElevenLabs REST API to list voices and confirms a given voice_id exists.
It does NOT use the official SDK (so it can run in this repo without extra deps).

Usage:
  python testcode/elevenlabs_voice_id_check.py --voice-id JBFqnCBsd6RMkjVDRZzb
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toc.env import load_env_files  # noqa: E402
from toc.http import HttpError, request_json  # noqa: E402


def _env(name: str, default: str | None = None) -> str | None:
    v = os.environ.get(name)
    if v is None or v == "":
        return default
    return v


def main() -> None:
    parser = argparse.ArgumentParser(description="Check if an ElevenLabs voice_id exists for your API key.")
    parser.add_argument("--voice-id", default="JOcmGzB8OFjY8MhjHHEf")
    parser.add_argument("--api-base", default=_env("ELEVENLABS_API_BASE", "https://api.elevenlabs.io/v1"))
    args = parser.parse_args()

    load_env_files(repo_root=REPO_ROOT)

    api_key = _env("ELEVENLABS_API_KEY") or ""
    if not api_key.strip():
        raise SystemExit("Missing ELEVENLABS_API_KEY (set env var or put it in .env).")

    base = str(args.api_base).rstrip("/")
    url = f"{base}/voices"

    try:
        data: dict[str, Any] = request_json(url=url, headers={"xi-api-key": api_key})
    except HttpError as e:
        raise SystemExit(str(e)) from e

    voices = data.get("voices") or []
    for v in voices:
        if not isinstance(v, dict):
            continue
        if str(v.get("voice_id") or "") == str(args.voice_id):
            name = v.get("name") or "<unknown>"
            category = v.get("category") or "<unknown>"
            print(f"OK: voice_id found: {args.voice_id} (name={name}, category={category})")
            return

    print(f"NOT FOUND: voice_id not in /voices for this API key: {args.voice_id}")


if __name__ == "__main__":
    main()
