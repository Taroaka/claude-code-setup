# ADR-0001: Spec-First を維持しつつ Root Guide を Pointer 化する

- Status: Accepted
- Date: 2026-03-09

## Context

ToC は `docs/` / `workflow/` / `scripts/` に正本を持つ spec-first リポジトリであり、
説明文書そのものが開発フローの一部になっている。

一方で Harness Engineering の観点では、root-level の長い guide はコンテキストを汚しやすく、
古い説明と最新の実装をエージェントが区別しにくい。

## Decision

- `docs/` / `workflow/` / `scripts/` を正本として維持する
- `AGENTS.md` / `CLAUDE.md` は同一内容の pointer doc に縮約する
- root guide には次だけ残す
  - 起点コマンド
  - 正本ドキュメントへのリンク
  - 禁止事項
  - 最小 verify 導線
- pointer doc の同一性と参照先 existence は機械検証する

## Consequences

- spec-first の思想は残る
- root から辿る導線は短くなり、Codex / Claude Code の初期コンテキスト負荷が下がる
- 詳細運用は `docs/implementation/assistant-tooling.md` など正本へ集約される
