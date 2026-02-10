# Requirements: Immersive Experience Variants（/toc-immersive-ride）

## Goal

既存の `/toc-immersive-ride`（没入型 First-person POV）で、従来の `ride_action_boat` に加えて
「哲学的な思考を要する概念を、雲上の島を歩いて理解を深める」体験テンプレ（`cloud_island_walk`）も扱えるようにする。

## In Scope

- `/toc-immersive-ride` に `--experience` を追加（default は従来互換の `ride_action_boat`）
- experience ごとに `video_manifest.md` の雛形（テンプレ）を用意
- 台本作成者（`immersive-scriptwriter`）が experience に合わせて prompt invariants と構成を選べるようにガイドを更新
- state 管理に experience を記録できる（`immersive.experience`）

## Out of Scope

- 画像/動画/TTS プロバイダの変更
- 生成スクリプトの大規模なスキーマ変更（manifest パーサーの破壊的変更）
- 既存の `ride_action_boat` 表現要件の緩和

## Success Criteria (MVP)

- `scripts/toc-immersive-ride.py --experience cloud_island_walk ...` で run dir が作られ、
  `workflow/` の cloud-island 用テンプレが `video_manifest.md` に反映される
- `cloud_island_walk` の manifest は `scripts/toc-immersive-ride-generate.sh`（`--apply-asset-guides --asset-guides-character-refs scene --require-character-ids`）前提でも破綻しない
- docs / agent guide に `--experience` と各 experience の表現方針が追記される

