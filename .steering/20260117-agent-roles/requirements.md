# Agent Roles & Prompts Requirements (Task 8)

## 目的
物語生成パイプラインにおける **役割分担・プロンプト仕様・検証責任** を定義する。

## 位置づけ
- 抽象方針は以下に準拠する：
  - `docs/story-creation.md`
  - `docs/script-creation.md`
  - `docs/orchestration-and-ops.md`
- 本書は「役割・プロンプトの要求」を定義し、設計詳細は `design.md` に記載する。

## スコープ
- Director / Scriptwriter / Reviewer / QA-Compliance の役割
- 各役割の入出力（期待フォーマット）
- プロンプトのバージョニング戦略
- Research出力の根拠（grounding / citation）ルール

## 非スコープ
- 実際のモデル選定やプロバイダ実装
- 生成UI/外部API設計

## 前提
- LLMはAPI利用（LangChain経由）
- 出力フォーマットは `workflow/*-template.yaml` を最小契約とする

## 役割要件

### Director（メイン）
- 入力: `research.md`
- 出力: `story.md`（`docs/story-creation.md`準拠）
- 物語構造/シーン設計の整合性を担保

### Scriptwriter（サブ）
- 入力: `story.md` + シーン計画
- 出力: `script.md`（`docs/script-creation.md`準拠）
- シーン単位での詳細台本作成

### Reviewer（Director兼務可）
- 入力: シーン/脚本
- 出力: accept / revise + 理由
- 連続性、世界観、制約遵守を確認

### QA / Compliance
- 入力: 研究・物語・動画成果物
- 出力: QAスコア + pass/fail + 指摘事項
- `docs/orchestration-and-ops.md` のQA/Compliance基準を適用

## プロンプト運用要件
- 役割ごとに **固定プロンプト + 動的コンテキスト** を分離する
- プロンプトにはバージョン番号を付与する

## Grounding / citation 要件
- Research段階の事実は source を必ず添付
- Story/Scriptの主張は research 参照を明示する

## 受け入れ条件
- 役割ごとの入出力と責務が明記されている
- プロンプト運用（バージョン管理/更新）が明確
- Groundingルールが定義されている
