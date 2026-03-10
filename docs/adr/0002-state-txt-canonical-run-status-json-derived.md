# ADR-0002: `state.txt` Canonical / `run_status.json` Derived

- Status: Accepted
- Date: 2026-03-09

## Context

ToC は `output/<topic>_<timestamp>/state.txt` を append-only の正本として採用している。
これは人間が追えることに価値がある。

一方で resume / CI / eval / report からは、機械処理しやすい JSON のほうが扱いやすい。

## Decision

- canonical state は引き続き `state.txt` とする
- machine-facing な派生状態として `run_status.json` を同じ run dir に生成する
- `run_status.json` は `state.txt` の flat/nested view、artifact inventory、pending gate、eval report を持つ
- `scripts/toc-state.py` と main scaffold scripts は state 更新時に JSON を同期する

## Consequences

- repo の人間可読 state 設計は維持される
- 自動検証・レポート・再開ロジックは JSON を読める
- `state.txt` と JSON の二重管理ではなく、片方が派生物として扱える
