# Orchestration Artifacts & Logging Design (Task 11)

## 目的
ジョブ単位で **再現可能な記録** を残し、調査/改善の材料にする。

## 参照
- `docs/orchestration-and-ops.md`
- `docs/data-contracts.md`

## 生成する成果物

```
output/<topic>_<timestamp>/
  orchestration_manifest.md
  run_report.md
  logs/
    RESEARCH_input.json
    RESEARCH_output.json
    STORY_input.json
    STORY_output.json
    SCRIPT_input.json
    SCRIPT_output.json
    VIDEO_input.json
    VIDEO_output.json
    QA_input.json
    QA_output.json
```

## マニフェスト仕様（要約）

- job_id / status / artifacts / gates / audit を記録
- `docs/orchestration-and-ops.md` のマニフェストを簡略化して使用

## ログ仕様

### 形式
- JSON（1ファイル=1ステージの入出力）
- 文字コード: UTF-8

### 最小フィールド

```json
{
  "job_id": "JOB_2026-01-17_0001",
  "stage": "STORY",
  "input": {...},
  "output": {...},
  "started_at": "ISO8601",
  "completed_at": "ISO8601",
  "duration_seconds": 12.3
}
```

## レビュー/QA記録

- Reviewer判定は `audit` に追記
- QAスコアは manifest に集約
- 重大指摘は `run_report.md` に要約

## ランレポート

### 目的
- コスト/時間/品質のサマリ
- 失敗原因と改善点の記録

### 最小構成
- job_id / topic / status
- total_duration / total_cost（推定）
- QAスコア
- 失敗や警告の一覧

## 受け入れ条件

- マニフェスト・ログ・レポートの配置が確定
- 各ログの最小フィールドが定義済み
