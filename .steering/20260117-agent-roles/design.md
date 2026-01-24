# Agent Roles & Prompts Design (Task 8)

## 目的
役割単位で責務を分離し、**再現性の高い出力**と**検証可能性**を確保する。

## 参照
- `docs/story-creation.md`
- `docs/script-creation.md`
- `docs/orchestration-and-ops.md`
- `docs/data-contracts.md`

## 実行モデル

- 起点は Claude Code の **slash command**
- 統括エージェントが `state.txt` を更新
- サブ作業は **skills** として呼び出す

## 役割と責務

### 1) Director（メイン）
- 目的: 物語全体の構成と一貫性を決定
- 入力: `research.md`
- 出力: `story.md`
- 参照: `docs/story-creation.md`
- 品質責務:
  - フック/物語構造/感情曲線の整合
  - 研究ソースの裏付け

### 2) Scriptwriter（サブ）
- 目的: シーン単位の詳細台本を作成
- 入力: `story.md` + scene plan
- 出力: `script.md`
- 参照: `docs/script-creation.md`
- 品質責務:
  - シーンの具体性
  - 視覚/音声の指示の明確性

### 3) Reviewer（Director兼務可）
- 目的: 連続性と制約遵守の検証
- 入力: scene draft / script
- 出力: `accept | revise` + 理由
- 品質責務:
  - 前後の脈絡
  - 世界観/キャラ/トーンの整合

### 4) QA / Compliance
- 目的: 正確性・一貫性・権利の最終チェック
- 入力: `research.md`, `story.md`, `script.md`, `video.mp4`
- 出力: QAスコア + pass/fail + 指摘
- 参照: `docs/orchestration-and-ops.md`

## プロンプト構成

各役割のプロンプトは **固定部** と **動的部** に分ける。

```
[固定部]
- 役割の目的
- 出力フォーマット
- 品質基準

[動的部]
- 入力成果物
- 制約（時間/比率/言語）
- 直近の指摘/リビジョン理由
```

## プロンプトバージョニング

- 形式: `role@vX.Y.Z`
- 変更履歴を `docs/prompt-changelog.md` に記録（作成予定）
- 重大変更は major を更新

## Grounding / citation ルール

- Research 出力は **source を必須**
- Story / Script は **research参照**を明示
- 生成物は `sources` セクションに記録

## 受け入れ条件

- 役割ごとに入出力と責務が明記されている
- プロンプト構成とバージョニングが明確
- Groundingルールが適用可能
