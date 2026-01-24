# Agent Roles & Prompts（正本）

このドキュメントは `.steering/20260117-agent-roles/` で合意した内容を **恒久仕様として昇華**したもの。

## 目的

役割単位で責務を分離し、再現性の高い出力と検証可能性を確保する。

## 実行モデル

- 起点は Claude Code の slash command
- 統括エージェントが `state.txt` を更新
- 役割別の振る舞いは `.claude/agents/*.md` に定義する（例: `director`）

## 役割と責務

### Director（監督）
- 入力: `research.md`
- 出力: `story.md`
- 参照: `docs/story-creation.md`
- エージェント定義: `.claude/agents/director.md`

### Scriptwriter
- 入力: `story.md` + scene plan
- 出力: `script.md`
- 参照: `docs/script-creation.md`

### Reviewer（Director兼務可）
- 入力: scene draft / script
- 出力: `accept | revise` + 理由

### QA / Compliance
- 入力: `research.md`, `story.md`, `script.md`, `video.mp4`
- 出力: QAスコア + pass/fail + 指摘
- 参照: `docs/orchestration-and-ops.md`

## プロンプト構成

固定部と動的部に分離する。

- 固定部: 役割の目的 / 出力フォーマット / 品質基準
- 動的部: 入力成果物 / 制約 / 直近の指摘・修正理由

## バージョニング

- 形式: `role@vX.Y.Z`
- 変更履歴は `docs/prompt-changelog.md`（将来作成）に集約する

## Grounding / citation

- Research 出力は source を必須化
- Story/Script は research 参照を明示する

## 参照

- `docs/story-creation.md`
- `docs/script-creation.md`
- `docs/orchestration-and-ops.md`
