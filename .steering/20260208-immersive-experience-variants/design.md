# Design: `--experience` によるテンプレ分岐 + 雲上の島（cloud_island_walk）

## 方針

- `experience` は **manifest テンプレ選択**のキーとして扱う
  - 実装ヘルパ（scaffold）でテンプレを切り替え、下流の生成スクリプトは manifest の契約通りに動くだけにする
- 互換性を優先し、default は従来の `ride_action_boat` のままにする

## Experience definitions

### `ride_action_boat`（既存）

- テーマパークのライド（ボート/安全バー）で世界を進む
- prompt のアンカーは「手 + brass safety bar」

### `cloud_island_walk`（新規）

- 雲上に浮かぶ“概念の楽園島”に到着し、歩くほど理解が深まる
- prompt のアンカーは構図で固定する（例: path/leading lines を常にセンター、地平線の安定、一定のカメラ高さ）
- 看板の文字で説明せず、**物理メタファ**（橋/鏡/結び目/重り等）で概念を表現する

## Manifest contract (MVP)

- `video_metadata.experience` を必須化（運用上の自己記述）
- `assets.style_guide.reference_images` に「手元アンカー参照画像」を入れられるようにする
  - `scripts/generate-assets-from-manifest.py --apply-asset-guides` が参照画像を scene 側へ自動マージする運用
- `scripts/toc-immersive-ride-generate.sh` の検証に通すため、各 scene の `image_generation.character_ids` は必ず明示（キャラ無しでも `[]`）

## Files / placement rationale

- テンプレ（契約）: `workflow/`（`*-template.md`）
- slash command ドキュメント: `.claude/commands/`
- 役割エージェントのガイド: `.claude/agents/`
- 正本仕様: `docs/implementation/`（entrypoint / prompting）
- 変更履歴（spec-first）: `.steering/20260208-immersive-experience-variants/`
