# Video Integration（正本）

このドキュメントは `.steering/20260117-video-integration/` で合意した内容を **恒久仕様として昇華**したもの。

## 目的

`script.md` から素材生成→合成→検証までを一貫した流れとして定義する。

## 全体フロー

`script.md → video_manifest.md → assets生成 → clips/narration list → render-video.sh → video.mp4 → QA`

## Scene → Assets 契約（最小）

入力（scene単位）:
- `scene_id`
- `narration_text`
- `visual_prompt`
- `duration_seconds`
- `constraints`
  - （任意）参照画像: `references[]`
  - （任意）動画の開始/終了フレーム: `first_frame`, `last_frame`

出力（scene単位）:
- `assets/scenes/scene{n}_base.png`
- `assets/scenes/scene{n}_video.mp4`
- `assets/audio/scene{n}_narration.mp3`

記録先:
- `video_manifest.md` の `scenes[]`

## プレースホルダ（MVP）

プロバイダは当面、manifestで選べる（例: Google Nano Banana Pro / Veo 3.1 / Kling 3.0）。ただしMVPでは:

- placeholder でE2Eを通す（`scripts/generate-placeholder-assets.py`）
- 生成APIで素材化する（`scripts/generate-assets-from-manifest.py`）

## 品質ゲート（最小）

- `duration_ok`
- `aspect_ratio_ok`
- `audio_sync_ok`
- `subtitle_ok`

結果は `state.txt` と `video_manifest.md` に記録する。

## 参照

- `docs/video-generation.md`
- `scripts/build-clip-lists.py`
- `scripts/render-video.sh`
