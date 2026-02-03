# Assistant tooling（Claude Code / Codex）仕様（正本）

このドキュメントは `.steering/20260131-improve-claude-code/` で合意した内容を **恒久仕様として昇華**したもの。

## 目的

ToCリポジトリに同梱されている `improve_claude_code/` を「置いてあるだけ」にせず、

- Claude Code で command pack / agents / skills を使える
- tmux multi-agent を Claude / Codex の両方で起動できる
- Codex 側でも運用（plan/tdd/verify 等）を再現できる

状態にする。

## 何がどこにあるか

### 同梱元（vendor）

- `improve_claude_code/`
  - `.claude/commands/`（汎用 slash command pack）
  - `agents/`（planner, code-reviewer 等）
  - `skills/`（tdd-workflow, verification-loop 等）
  - `shutsujin_departure.sh`（tmux multi-agent 起動）

### ToC側（実際に使う場所）

- Claude Code:
  - `.claude/commands/improve/`（上記 command pack を同期）
  - `.claude/agents/`（agents を同期）
  - `.claude/skills/`（skills を同期）
- Codex:
  - `codex_skills/`（Codex skill のソース）
  - `scripts/ai/install-codex-skills.sh`（`~/.codex/skills` へインストール）

## Claude Code: コマンド/エージェント/スキル

- 追加されたコマンドは `.claude/commands/improve/` 配下（例: `/plan`, `/tdd`, `/verify`, `/code-review`）
- 追加されたエージェントは `.claude/agents/` 配下（例: `planner.md`, `code-reviewer.md`）
- 追加されたスキルは `.claude/skills/` 配下（例: `tdd-workflow/`, `verification-loop/`）

## tmux multi-agent（Claude / Codex）

このリポジトリでは `scripts/ai/multiagent.sh` を起点にする。

```bash
# Claude Code で起動
scripts/ai/multiagent.sh --engine claude

# Codex CLI で起動
scripts/ai/multiagent.sh --engine codex
```

前提:
- `tmux` が必要（macOS 例: `brew install tmux`）

## ToCの並列開発（推奨パターン）

「research → story/script → scene雛形 → scene別制作」は依存が強いので、共有ファイルを複数足軽が同時編集しない。

- Phase 1（並列）: 各足軽は `scratch/ashigaruN/research_notes.md` に調査結果を書き、**1人が research.md に統合**
- Phase 2（並列）: 各足軽は `scratch/ashigaruN/story_notes.md` に案を書き、**1人が story.md（or script.md）に統合**
- Phase 3（直列）: **1人**が `scripts/toc-scene-series.py` で `scenes/` を雛形生成
- Phase 4（並列）: sceneごとに `scenes/sceneXX/` 配下だけ編集して完成（競合なし）
- Phase 5（直列）: **1人**が全体サマリ作成

準備スクリプト（scratch/run-dir作成）:

```bash
python scripts/ai/toc-scene-series-multiagent.py "topic"
```

## Codex: improve-workflow skill

- スキルソース: `codex_skills/improve-workflow/`
- インストール:

```bash
scripts/ai/install-codex-skills.sh
```

インストール先（グローバル）:
- `~/.codex/skills/improve-workflow/`

## Claude Code: rules（任意・グローバル）

`improve_claude_code/rules/*.md` を `~/.claude/rules/` にコピーしてグローバルに適用する。

```bash
scripts/ai/install-claude-rules.sh
```

※ 影響範囲は全プロジェクトになるため、不要なら削除/運用で調整する。
