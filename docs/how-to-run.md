# How to Run (MVP)

本書は `todo.txt` の 15) Documentation に対応する。

## 前提
- 起点は Claude Code の slash command（例: `/toc-run`, `/toc-scene-series`, `/toc-immersive-ride`）
- 成果物は `output/<topic>_<timestamp>/` に生成される
- state は `output/<topic>_<timestamp>/state.txt`（追記型）

## セットアップ（Docker）

1) `.env.example` を `.env` にコピーし、APIキー等を設定する  
2) 起動:

```bash
docker-compose up --build
```

## セットアップ（uv / local）

uv で依存を揃える場合（.venv を作って同期）:

```bash
python -m pip install -U uv
scripts/uv-sync.sh
```

## 実行（想定）

Claude Code で以下を実行:

```
/toc-run "桃太郎" --dry-run
```

sceneごとにQ&A動画を複数本作る場合:

```
/toc-scene-series "桃太郎" --min-seconds 30 --max-seconds 60
```

没入型（First-person POV）実写ライド体験の単発動画:

```text
/toc-immersive-ride --topic "桃太郎"
```

## 期待される出力（/toc-run）

```
output/<topic>_<timestamp>/
  state.txt
  research.md
  story.md
  script.md
  video_manifest.md
  video.mp4          (プレースホルダでも可)
  run_report.md
  logs/
```

## 期待される出力（/toc-scene-series）

```
output/<topic>_<timestamp>/
  state.txt
  research.md
  story.md
  series_plan.md
  scenes/
    scene01/
      evidence.md
      script.md
      video_manifest.md
      assets/
      video.mp4
    scene02/
      ...
```

## 生成（画像/動画/TTS）について

- 画像: Google Nano Banana Pro（Gemini Image / `gemini-3-pro-image-preview`）
- 画像（代替）: SeaDream / Seedream 4.5（`tool: "seadream"` + `SEADREAM_*`）
- 動画: Google Veo 3.1（`video_generation.tool: "google_veo_3_1"`）
- 動画（代替）: Kling 3.0（`video_generation.tool: "kling_3_0"` + `KLING_*`）
- TTS: ElevenLabs
- 当面は `video_manifest.md` を入力に素材生成→結合でフローを検証する
- 具体は `docs/implementation/video-integration.md` を参照

例（`momotaro` のマニフェストから素材生成→結合）:

```bash
python scripts/generate-assets-from-manifest.py \
  --manifest output/momotaro_20260110_1700/video_manifest.md \
  --character-reference-views front,side,back \
  --character-reference-strip \
  --image-batch-size 10 --image-batch-index 1 \
  # --skip-audio を外すと ElevenLabs でナレーション生成も行う

python scripts/build-clip-lists.py \
  --manifest output/momotaro_20260110_1700/video_manifest.md \
  --out-dir output/momotaro_20260110_1700

scripts/render-video.sh \
  --clip-list output/momotaro_20260110_1700/video_clips.txt \
  --narration-list output/momotaro_20260110_1700/video_narration_list.txt \
  --out output/momotaro_20260110_1700/video.mp4
```

## state運用

- `state.txt` は追記型（最新ブロックが現在状態）
- 擬似ロールバックは「過去ブロックのコピーを末尾に追記」で再現する
- スキーマは `workflow/state-schema.txt` を参照
