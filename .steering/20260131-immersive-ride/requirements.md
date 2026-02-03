# Immersive Ride POV Slash Command: Requirements

## Goal

トピック入力を起点に、

1) Deep Research
2) 台本作成（没入型：First-person POV / 実写シネマ）
3) 画像生成（参照画像つき）
4) 動画生成（Veo 3.1 / first-last-frame-to-video）
5) 結合・エンコード（ffmpeg）

を **1つの工程**として完了させるための **新しい slash command** を追加する。

## Command (proposed)

- Name: `/toc-immersive-ride`
- Args:
  - `--topic`（必須）
  - `--dry-run`（任意。外部APIは呼ばない）
  - `--config`（任意。`config/system.yaml` 互換）

## Finished Video Spec (must)

- Total duration: narration（音声）の尺に合わせる
- Resolution: **1280x720 (16:9)**
- Frame rate: **24fps**
- Style: **photorealistic / cinematic / practical effects**（アニメ調排除）
- POV: **First-person POV** を一貫
- Unified elements:
  - 20代女性の手
  - ornate brass safety bar
  - theme park “ride action boat” vehicle（線路に沿って進む）
  - キャラクターが毎scene必ず登場

## Providers (assumed)

- Image: Google Nano Banana Pro（Gemini Image / `gemini-3-pro-image-preview`）
  - Multi-image reference（キャラクター・手/ボート参照）を活用
  - Output image: 16:9 / 2K（素材側）
- Video: Google Veo 3.1（`veo-3.1-generate-preview`）
  - first-last-frame-to-video
  - 8 seconds / 16:9
- TTS: ElevenLabs（男性 / calm, mystical storytelling）

## Output Layout

`output/<topic>_<timestamp>/`

- `state.txt`（追記型）
- `research.md`（deep research の要約・参照先を含む）
- `story.md`
- `script.md`（没入型ライドPOV用）
- `video_manifest.md`（生成契約の中心）
- `assets/**`（characters/styles/scenes/audio）
- `video.mp4`（最終）
- `run_report.md`（任意）

## Core Prompt Rules

### DO

- 全プロンプトに固定フレーズを含める:
  - `First-person POV from ride action boat`
  - `Realistic hands gripping ornate brass safety bar`
- 参照画像を **全生成** に含める（キャラクター・手/バー・ボート等）
- 連続性:
  - sceneの終了が次sceneの開始につながる
  - 照明・雰囲気が自然に遷移
  - ボートは線路に沿って進む（中央配置/曲線/イベント配置）

### DON'T

- anime/cartoon/illustration 方向の指示
- 曖昧な指示（例: “magical” のみ）
- 視点のブレ（手とバーが常に画面内）

## Non-goals (MVP)

- 自動字幕（SRT）生成
- 高度な編集（BGM/SFXの自動設計、複雑なカット割り）
- プロンプト最適化の反復（選定・再生成の自動ループ）

