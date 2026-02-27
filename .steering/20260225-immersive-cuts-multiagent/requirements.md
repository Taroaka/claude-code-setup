# Requirements: Immersive cuts multi-agent (scene2+)

## Goal

`/toc-immersive-ride` の run dir（例: `output/<topic>_<timestamp>_immersive/`）にある `video_manifest.md` について、
scene2 以降の各 scene を **cuts（3〜5）** に分割し、画像生成要素（カット）を増やす。

この cuts の **数と内容は scene 担当のサブエージェント（並列ワーカー）が考える**。

## Non-Goals

- 画像生成/動画生成をこの変更で自動実行する（APIコール）はしない
- 既存の生成プロバイダ実装や `generate-assets-from-manifest.py` の仕様変更はしない
- 既存 run dir の大規模な構造変更（scene-series の `scenes/sceneXX/` 方式へ移行）はしない

## Constraints / Principles

- 共有ファイル `video_manifest.md` は **同時編集しない**（single-writer で統合）
- 並列化は `scratch/` に scene別の成果物を置き、最後に 1人がマージする
- `scripts/generate-assets-from-manifest.py` が解釈できる YAML 構造（`scenes[].cuts[]`）を維持する

## Acceptance Criteria

- `run_dir/scratch/cuts/sceneXX.yaml` を各scene分作成できる
- scene2+ について `video_manifest.md` の YAML を `cuts` 形式へ安全にマージできる
- マージ後の `video_manifest.md` が `generate-assets-from-manifest.py --dry-run` でパースできる
- マージスクリプトが「次に起動するコマンド」を明示してユーザーへ促す

