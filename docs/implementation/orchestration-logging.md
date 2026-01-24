# Orchestration Artifacts & Logging（正本）

このドキュメントは `.steering/20260117-orchestration-logging/` で合意した内容を **恒久仕様として昇華**したもの。

## 目的

ジョブ単位で再現可能な記録（manifest / logs / report）を残し、調査/改善の材料にする。

## 出力構成

```
output/<topic>_<timestamp>/
  orchestration_manifest.md
  run_report.md
  logs/
    <STAGE>_input.json
    <STAGE>_output.json
```

## ログ（最小フィールド）

```json
{
  "job_id": "JOB_YYYY-MM-DD_0001",
  "stage": "STORY",
  "input": {},
  "output": {},
  "started_at": "ISO8601",
  "completed_at": "ISO8601",
  "duration_seconds": 0.0
}
```

## 参照

- `docs/orchestration-and-ops.md`
- `docs/data-contracts.md`
