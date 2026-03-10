#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$repo_root"

echo "== CWD =="
pwd

echo
echo "== Git Status =="
git status --short || true

echo
echo "== Recent Commits =="
git log --oneline -5 || true

latest_run="$(fd . output -t d -d 1 2>/dev/null | sort | tail -1 || true)"

echo
echo "== Latest Run =="
if [[ -n "${latest_run}" ]]; then
  echo "$latest_run"
  if [[ -f "$latest_run/state.txt" ]]; then
    echo
    echo "== Pending Gates =="
    python scripts/toc-state.py show --run-dir "$latest_run" || true

    echo
    echo "== Fast Verify =="
    if [[ -d "$latest_run/scenes" ]]; then
      python scripts/verify-pipeline.py --run-dir "$latest_run" --flow scene-series --profile fast || true
    elif [[ -f "$latest_run/video_manifest.md" ]]; then
      python scripts/verify-pipeline.py --run-dir "$latest_run" --flow immersive --profile fast || true
    fi
  fi
else
  echo "No run directories found under output/."
fi
