# Entrypoint（/toc-immersive-ride）仕様（正本）

このドキュメントは `.steering/20260131-immersive-ride/` で合意した内容を **恒久仕様として昇華**したもの。

## 目的

Claude Code の slash command を起点に、最小限の入力（topic）で
「没入型（First-person POV）実写シネマ・ライド体験」動画を **1本**生成する。

## 仕様（想定）

- コマンド: `/toc-immersive-ride`
- 引数:
  - `--topic`（必須）
  - `--dry-run`（任意。外部生成APIは呼ばない）
  - `--config`（任意。`config/system.yaml` を差し替え）

## 挙動（成果物）

run root:

- `output/<topic>_<timestamp>/`
  - `state.txt`（追記型）
  - `research.md`
  - `story.md`
  - `script.md`
  - `video_manifest.md`
  - `assets/**`
  - `video.mp4`（完成。1280x720 / 24fps）

## 表現の固定条件（必須）

- POV: First-person POV（視点固定）
- Style: photorealistic / cinematic / practical effects（アニメ調排除）
- 統一要素:
  - 20代女性の手
  - ornate brass safety bar
  - ride action boat（線路に沿って進む）
  - キャラクターが毎scene登場

## 生成設計（最小）

- 画像:
  - 参照画像（キャラクター/手/ボート）を **全scene** に適用
  - 16:9 / 2K（素材側）
- 動画:
  - Veo 3.1 / first-last-frame-to-video
  - 8秒/clip
  - scene画像の隣接ペアをつないでclipを作る（first frame = scene_n.png / last frame = scene_{n+1}.png）
  - シームレス性を上げるため、best-effort で以下を併用する
    - `last_frame` 制約（`--enable-last-frame`）
    - ネガティブプロンプトでフェード/カット系を抑制（`--video-negative-prompt`）
    - 直前clip終盤のフレームを次clipの first frame に使う chaining（`--chain-first-frame-from-prev-video`）
- 音声:
  - ElevenLabs（男性 / calm, mystical storytelling）
  - run root に単一音声として生成し、最終結合で合わせる
  - 反復中は音声を省略してサイレントで書き出してよい（`--skip-audio`）

## コスト最適化（任意）

- `GEMINI_VIDEO_MODEL` を fast/cheap 系に切り替える（例: `veo-3.1-fast-generate-preview`）

## state（追記）

`state.txt` に追記（例）:

- `runtime.stage=research|story|script|manifest|assets|render|done`

## 参照

- `.claude/commands/toc/toc-immersive-ride.md`
- `docs/how-to-run.md`
- `docs/implementation/video-integration.md`
