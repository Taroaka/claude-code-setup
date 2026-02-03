#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SRC_DIR="$REPO_ROOT/improve_claude_code/rules"
DEST_DIR="$HOME/.claude/rules"

if [[ ! -d "$SRC_DIR" ]]; then
  echo "[ERROR] improve_claude_code/rules not found at: $SRC_DIR" >&2
  exit 1
fi

mkdir -p "$DEST_DIR"

installed=0
for rule_path in "$SRC_DIR"/*.md; do
  [[ -f "$rule_path" ]] || continue

  base_name="$(basename "$rule_path")"
  dest_path="$DEST_DIR/improve_claude_code_${base_name}"

  cp "$rule_path" "$dest_path"
  installed=$((installed + 1))
  echo "[OK] Installed: $dest_path"
done

if [[ "$installed" -eq 0 ]]; then
  echo "[WARN] No .md rule files found in: $SRC_DIR" >&2
fi

