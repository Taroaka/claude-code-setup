# Pipeline Evals

このディレクトリは ToC の stage-gated harness の正本です。

- `golden-topics.yaml`: 回帰用トピックの固定セット
- `workflow/evaluation_criteria.md`: stage 評価の親仕様

この repo の評価は exact text 一致を狙わない。
見るのは次の3点です。

- 必要構造があるか
- 必要根拠が残っているか
- 必要 gate を通過できるか
