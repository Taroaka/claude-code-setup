# QA / Evaluation Harness（正本）

このドキュメントは `.steering/20260117-qa-harness/` で合意した内容を **恒久仕様として昇華**したもの。

## 方針

- 人間レビューを標準とする
- 自動チェックは `scripts/verify-pipeline.py` に集約する
- 自動評価は stage ごとの gate とし、全体再生成ではなく failing stage の切り分けに使う

## 回帰トピック（例）

- 桃太郎
- 竹取物語
- 浦島太郎

## 自動レビュー

```bash
python scripts/verify-pipeline.py \
  --run-dir output/<topic>_<timestamp> \
  --flow toc-run|scene-series|immersive \
  --profile fast|standard
```

成果物:

- `eval_report.json`
- `run_report.md`

## 手動レビュー

- `docs/orchestration-and-ops.md` の QA チェックリストに沿って評価
- 結果は `run_report.md` に記録する

## 参照

- `docs/orchestration-and-ops.md`
- `workflow/evaluation_criteria.md`
