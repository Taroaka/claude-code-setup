# Orchestration Artifacts & Logging Requirements (Task 11)

## 目的
オーケストレーションの各ステップを **追跡可能** にし、
成果物・ログ・レビュー結果を再現できるようにする。

## 参照
- `docs/orchestration-and-ops.md`
- `docs/data-contracts.md`
- `workflow/video-manifest-template.md`

## スコープ
- オーケストレーション・マニフェスト
- ノード入出力ログ
- レビュー/QA結果の保存
- ランレポートの生成

## 前提
- state管理は `state.txt`（追記型）
- 主要成果物は `output/<topic>_<timestamp>/`

## 要件

### マニフェスト
- `output/<topic>_<timestamp>/orchestration_manifest.md` を生成
- job_id / status / artifacts / gates / audit を記録

### ログ
- 各ノードの **入力/出力** を記録
- ログは `output/<topic>_<timestamp>/logs/` に保存

### レビュー結果
- review判断（accept/revise）と理由を保存
- QAスコアはmanifestに集約

### ランレポート
- 1ジョブ1レポート（コスト/時間/品質）
- `output/<topic>_<timestamp>/run_report.md`

## 受け入れ条件
- マニフェスト/ログ/レポートの保存先が明確
- ログの最小構造が定義されている
