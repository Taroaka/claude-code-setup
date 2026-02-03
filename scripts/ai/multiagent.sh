#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
IMPROVE_DIR="$REPO_ROOT/improve_claude_code"

ENGINE="claude"
INSTALL_TMUX=false

usage() {
  cat << 'EOF'
Usage:
  scripts/ai/multiagent.sh [--engine claude|codex] [--install-tmux] -- [args forwarded]

Examples:
  # Claude Code で multi-agent 起動
  scripts/ai/multiagent.sh --engine claude

  # Codex CLI で multi-agent 起動
  ｆ

  # tmux 未導入の macOS で自動インストールして起動
  scripts/ai/multiagent.sh --install-tmux --engine claude

Notes:
  - 実体は improve_claude_code/shutsujin_departure.sh を呼び出します
  - improve 側のオプション（-s/--setup-only, -t/--terminal, -shell/--shell 等）はそのまま渡せます
EOF
}

forward_args=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    -e|--engine)
      if [[ $# -lt 2 ]]; then
        echo "[ERROR] --engine requires value: claude|codex" >&2
        exit 1
      fi
      ENGINE="$2"
      shift 2
      ;;
    --install-tmux)
      INSTALL_TMUX=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      forward_args+=("$@")
      break
      ;;
    *)
      forward_args+=("$1")
      shift
      ;;
  esac
done

case "$ENGINE" in
  claude|codex) ;;
  *)
    echo "[ERROR] Unsupported engine: $ENGINE (expected: claude|codex)" >&2
    exit 1
    ;;
esac

if [[ ! -d "$IMPROVE_DIR" ]]; then
  echo "[ERROR] improve_claude_code not found at: $IMPROVE_DIR" >&2
  exit 1
fi

cd "$REPO_ROOT"

ensure_symlink() {
  local dest="$1"
  local target="$2"

  if [[ -L "$dest" ]]; then
    return 0
  fi
  if [[ -e "$dest" ]]; then
    echo "[WARN] Exists and is not a symlink; skipping: $dest" >&2
    return 0
  fi

  ln -s "$target" "$dest"
}

# Make multi-agent artifacts visible from repo root (so tasks can refer to ./queue, ./instructions, ./dashboard.md).
ensure_symlink "$REPO_ROOT/queue" "$IMPROVE_DIR/queue"
ensure_symlink "$REPO_ROOT/instructions" "$IMPROVE_DIR/instructions"
ensure_symlink "$REPO_ROOT/memory" "$IMPROVE_DIR/memory"
ensure_symlink "$REPO_ROOT/status" "$IMPROVE_DIR/status"
ensure_symlink "$REPO_ROOT/dashboard.md" "$IMPROVE_DIR/dashboard.md"

if ! command -v tmux >/dev/null 2>&1; then
  if [[ "$INSTALL_TMUX" == true && "$(uname -s)" == "Darwin" ]]; then
    if command -v brew >/dev/null 2>&1; then
      echo "[INFO] Installing tmux via Homebrew..."
      brew install tmux
    else
      echo "[ERROR] Homebrew not found. Install tmux manually." >&2
      exit 1
    fi
  else
    cat << 'EOF' >&2
[ERROR] tmux not found.

Install examples:
  - macOS:  brew install tmux
  - Ubuntu: sudo apt-get install -y tmux

Or re-run on macOS with:
  scripts/ai/multiagent.sh --install-tmux --engine claude
EOF
    exit 1
  fi
fi

if [[ "${#forward_args[@]}" -gt 0 ]]; then
  exec "$IMPROVE_DIR/shutsujin_departure.sh" --engine "$ENGINE" "${forward_args[@]}"
fi

exec "$IMPROVE_DIR/shutsujin_departure.sh" --engine "$ENGINE"
