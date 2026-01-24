# QA / Evaluation Harness（正本）

このドキュメントは `.steering/20260117-qa-harness/` で合意した内容を **恒久仕様として昇華**したもの。

## 方針

- 人間レビューを標準とする
- 任意の自動チェックは「完成物評価後」に限り実施可
  - 影響範囲は指摘箇所のみ（全体再生成はしない）

## 回帰トピック（例）

- 桃太郎
- 竹取物語
- 浦島太郎

## 手動レビュー

- `docs/orchestration-and-ops.md` の QA チェックリストに沿って評価
- 結果は `run_report.md` に記録する

## 参照

- `docs/orchestration-and-ops.md`
