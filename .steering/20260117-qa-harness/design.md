# QA / Evaluation Harness Design (Task 13)

## 目的
生成品質を **手動QA中心** で評価し、再現可能な検証手順を整える。

## 参照
- `docs/orchestration-and-ops.md`
- `.steering/20260117-qa-harness/requirements.md`

## 方針
- 人間レビューを標準とする
- **任意の自動チェック**は実施可（デフォルトは未実施）
  - 実施タイミング: **完成物の評価後**
  - 影響範囲: **指摘された箇所のみ修正**

## 回帰テストセット

固定トピック例:
- 桃太郎
- 竹取物語
- 浦島太郎

※ テーマ追加は `tests/topics.txt` に追記する想定

## 手動レビュー手順

1. `research.md` / `story.md` / `script.md` / `video.mp4` を確認
2. `docs/orchestration-and-ops.md` のQAチェックリストに沿って評価
3. 結果を `run_report.md` に記録

## 任意の自動チェック（オプション）

- 目的: 手動評価後の **局所的な指摘箇所** を補助的に検証
- 実施条件: エージェントが完了後、**完成物に対する評価を行った場合のみ**
- 作用: 指摘箇所以外には影響しない（全体再生成はしない）

## 出力

- `output/<topic>_<timestamp>/run_report.md`

## 受け入れ条件

- 回帰セットの運用ルールが定義済み
- QAの評価が再現できる
