# Improve Claude/Codex Developer Experience: Tasklist

## 1) Spec / docs

- [ ] `.steering/20260131-improve-claude-code/` を作成（requirements/design/tasklist）
- [ ] `docs/implementation/` に正本（導入/使い方）を追加
- [ ] `docs/README.md` にリンク追加

## 2) Claude Code integration（B）

- [ ] `improve_claude_code/.claude/commands/*` を `.claude/commands/improve/` へ同期
- [ ] `improve_claude_code/agents/*` を `.claude/agents/` へ同期
- [ ] `improve_claude_code/skills/*` を `.claude/skills/` へ同期
- [ ] 既存 ToC の `.claude/commands/toc/*` が壊れていないことを確認

## 3) Multi-agent launcher（C + D-1）

- [ ] `improve_claude_code/shutsujin_departure.sh` を `--engine claude|codex` 対応に拡張
- [ ] ToC側に `scripts/ai/multiagent.sh`（薄いラッパ）を追加
- [ ] macOS で `tmux` 導入手順を追加（必要なら `brew install tmux` を案内）

## 4) Codex Skill（D-2）

- [ ] `codex_skills/improve-workflow/` を作成（SKILL.md）
- [ ] `scripts/ai/install-codex-skills.sh` を追加（`~/.codex/skills` へコピー）
- [ ] インストール後、`~/.codex/skills/improve-workflow/SKILL.md` が存在することを確認

## 5) Validation

- [ ] `python -m compileall .`（最低限の構文チェック）
- [ ] 追加したシェルスクリプトの `shellcheck` 相当は無しでも、`bash -n` で構文チェック
