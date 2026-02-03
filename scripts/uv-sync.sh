#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Create a local venv and sync pinned dependencies using uv.

Usage:
  scripts/uv-sync.sh

Notes:
- Creates/updates .venv/ (gitignored)
- Uses requirements.txt (generated from requirements.in)
USAGE
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ ! -f "requirements.txt" ]]; then
  echo "[ERROR] requirements.txt not found. Generate it first:" >&2
  echo "  python -m uv pip compile requirements.in -o requirements.txt" >&2
  exit 1
fi

python -m uv venv .venv
python -m uv pip sync --python .venv requirements.txt

echo "Synced venv: .venv"
