# Improve Claude/Codex Developer Experience: Requirements

## Goal

`improve_claude_code/` に同梱されている「Claude Code強化セット（commands / agents / skills / rules / multi-agent tmux）」を、
このToCリポジトリでも **実際に使える状態**にする。

加えて、Claude Code だけでなく **Codex CLI でも同等の運用**ができるようにする。

## Scope (ABC + D)

### A) 理解

- `improve_claude_code/` が「何のための何の集まりか」を、ToC視点で説明できる

### B) Claude Code へ適用

- ToCリポジトリの `.claude/` から、`improve_claude_code` の command pack / agents / skills を利用できる
- 既存の ToC 用 slash command（`/toc-run`, `/toc-scene-series`）は壊さない
- 変更は最小・衝突回避（ファイル名重複など）を優先

### C) Multi-agent（tmux）を使える

- `improve_claude_code` の `shutsujin_departure.sh` を、ToCから起動しやすい導線を作る
- macOS でも「必要条件（tmuxなど）」が満たせる導入手順を用意する

### D) Codex CLI でも適用

- Multi-agent（tmux）を Claude Code だけでなく Codex CLI でも起動できる（同じ構成で切り替え可能）
- Codex 側にも「plan / tdd / verify / code-review などの運用」を再現するための **Codex Skill** を用意する

## Non-goals (for now)

- `improve_claude_code/` の上流（everything-claude-code / multi-agent-shogun）への追従戦略の確立
- ToC本体のワークフロー（動画生成フロー）の設計変更
- 既存 `.claude/settings*.json` の挙動を大きく変えるような強制Hook導入（必要なら後続タスク）

## Success criteria

- `.claude/commands` に新しい command pack が増え、Claude Code から認識される
- `.claude/agents` / `.claude/skills` に追加物が入り、既存と衝突しない
- `scripts/` 経由で multi-agent を `claude` / `codex` のどちらでも起動できる
- Codex Skill が `~/.codex/skills/` にインストールでき、以後のセッションで利用できる

