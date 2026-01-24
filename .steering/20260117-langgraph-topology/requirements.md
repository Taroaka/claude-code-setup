# LangGraph Topology Requirements (Task 7)

## 目的
LangGraphのトポロジ（状態・遷移・ゲート・再試行）の要件を定義し、以降の設計・実装の基準とする。

## 位置づけ
- 既存の抽象要件は以下に準拠する：
  - `docs/system-architecture.md`
  - `docs/orchestration-and-ops.md`
  - `docs/data-contracts.md`
- 本書は「トポロジの要求」を定義し、設計詳細は `design.md` に記載する。

## スコープ
- 対象：LangGraph上のステートマシン、レビューゲート、QA再試行、監査ログの要件
- 非対象：具体的なプロバイダ実装、APIサーバー、配信/分析パイプライン

## 前提
- MVPはローカル/Claude Code（slash command）運用
- LLMはAPI利用（LangChain経由）
- 状態は **プロジェクトフォルダの `state.txt`** で管理（追記型）
- 状態スキーマは `workflow/state-schema.txt` に準拠

## 機能要件

### 必須ステート
以下のトップレベルステートを持つこと：
- `INIT → RESEARCH → STORY → SCRIPT → VIDEO → QA → DONE`

### レビューゲート
- `research_review` / `story_review` / `video_review` を持つこと
- ゲート値は `required | optional | skipped` を取ること
- デフォルトは `docs/orchestration-and-ops.md` に準拠

### QA再試行
- `accuracy_score < 0.75` → `RESEARCH` を再実行
- `engagement_score < 0.7` → `STORY` を再実行
- `consistency_score < 0.7` → `VIDEO` を再実行
- 再試行回数の上限は設計で決定する

### シーン単位の反復
- `SCRIPT` 内で、シーン単位の作成とレビューの反復を支援できること
- `VIDEO` 内で、シーン単位の素材生成と検証を支援できること

### 監査ログ
- 各ステート遷移に対し、最低限以下を記録すること：
  - step, status, reviewer, notes, reviewed_at

## 非機能要件
- 途中停止からの再開が可能なこと（チェックポイント前提）
- トレース可能性（入力/出力/判断の追跡）が確保されること

## 受け入れ条件
- 上記ステートとゲート/再試行条件を満たすトポロジ設計が完成している
- `design.md` で状態遷移図と失敗時の挙動が明確に記述されている
