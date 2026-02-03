# Immersive Ride POV Slash Command: Design

## Overview

単発の完成動画（1本）を生成するためのエントリポイントを追加する。

`/toc-run` と異なる点は、**没入型（First-person POV）・実写シネマ・ライド体験**の制約を
台本/マニフェストに強く織り込み、下流の画像/動画生成を **参照画像つき**で行うこと。

## High-level flow

```text
TOPIC (--topic)
  → RESEARCH (deep-researcher) -> output/research/<topic>_*.md
  → STORY (director)           -> output/<run>/story.md
  → SCRIPT (immersive-scriptwriter) -> output/<run>/script.md + video_manifest.md
  → GENERATE_ASSETS (API)      -> assets/**
  → RENDER (ffmpeg)            -> video.mp4 (1280x720, 24fps)
```

## Contracts

### `video_manifest.md` (run root)

目的: 既存の素材生成パイプライン（`scripts/generate-assets-from-manifest.py`）で
「画像→動画→音声」を生成でき、かつ **first-last-frame-to-video** を表現できること。

拡張点（今回追加）:

- Image generation:
  - `references: [<path>, ...]`（参照画像の配列）
- Video generation:
  - `first_frame: <path>`（開始フレーム）
  - `last_frame: <path>`（終了フレーム）

後方互換:
- 既存の `input_image` は `first_frame` のエイリアスとして扱う

### Resolution / fps

最終出力は `scripts/render-video.sh` で 1280x720 / 24fps に揃える（オプション追加で吸収）。

## Scene / Clip strategy

- 「scene画像」を N枚生成
- 「scene i → scene i+1」を 8秒動画（Veo）として生成し、`clips.txt` に並べる
- ナレーションは run root の単一音声（ElevenLabs）とし、`render-video.sh --audio` で合成する

## State tracking

`output/<run>/state.txt` に追記:

- `runtime.stage=research|story|script|manifest|assets|render|done`

