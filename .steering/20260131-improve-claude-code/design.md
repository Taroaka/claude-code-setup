# Improve Claude/Codex Developer Experience: Design

## Overview

このToCは `.claude/` を使ってClaude Codeの slash command / agents / skills を管理している。
一方で `improve_claude_code/` は別リポジトリ相当の強化セットとして同梱されているが、現状は **ToC本体から参照されず、使い方が分かりにくい**。

本対応では、ToC側に **導線（同期/起動/説明）**を追加して「置いてあるだけ」状態を解消する。

## Claude Code への取り込み方針（B）

- `improve_claude_code/` を「vendor（同梱ソース）」として維持しつつ、ToCの `.claude/` に **必要物を同期**する
- 同期先は、既存 ToC コマンドと衝突しないように **サブディレクトリ**に配置する
  - commands: `.claude/commands/improve/`
- agents / skills は Claude Code 側の探索仕様が不明確なため **トップレベルに配置**する（現状衝突なし）
  - agents: `.claude/agents/`
  - skills: `.claude/skills/`
- 同期は「コピー」方式（symlinkはOS差分/権限差分があるため避ける）

## Multi-agent（tmux）の導線（C）

- 実体は `improve_claude_code/shutsujin_departure.sh` を使う
- ToC側は `scripts/ai/multiagent.sh` を用意し、`--engine claude|codex` を選べるようにする
- macOS で `tmux` が無い場合は `brew install tmux` を案内（自動インストールは任意）

## Codex対応（D）

### D-1: tmux起動をCodexにも対応

- `improve_claude_code/shutsujin_departure.sh` を拡張し、起動コマンドを `claude` 以外（`codex`）にも切替可能にする
  - 例: `--engine codex` のとき `codex -m gpt-5-codex --config model_reasoning_effort=xhigh` を起動
  - `--setup-only` のときは起動せず、tmuxセッションだけ作る（従来通り）

### D-2: Codex Skill の追加

- `codex_skills/` にスキルソースを置き、`scripts/ai/install-codex-skills.sh` で `~/.codex/skills/` へインストールする
- スキルは「improve_claude_code の command pack 相当（plan/tdd/verify/code-review 等）を Codex でも再現」することに特化し、
  ToC固有の動画生成フローは対象外（それは既存AGENTS/CLAUDEの範囲）

## Docs（使い方の置き場所）

- 永続仕様として `docs/implementation/` に「AI支援ツールの使い方（Claude/Codex + multi-agent）」を追加する
- `docs/README.md` にリンクを追加して迷子を減らす
