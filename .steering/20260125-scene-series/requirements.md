# Scene-Series Slash Command: Requirements

## Goal

トピック入力を起点に、

1) 情報収集（Deep Research）
2) 縦型動画の生成

を **1つの工程**として完了させるための **第2の slash command** を追加する。

この第2コマンドは「物語の各シーン = 1本の動画（Q&A）」を生成することに特化する。

## User decisions (confirmed)

- Command name: 任意（ToC配下の一貫した命名にする）
- Scene video length: **30–60 seconds**
- Evidence strategy: **既存の `research.md` を優先**し、不足時のみ追加調査（Web検索）
- Output layout: **1 topic 1 run フォルダ**の配下に `scenes/sceneXX/` を切る

## Core concept (what it does)

- `story.md`（または `script.md`）に存在する各シーンの `text_overlay.sub_text` を **問い（question）** とみなす
- 各questionに対して「回答（answer）と根拠（evidence）」を作り、その内容を30–60秒の縦動画として出力する
- **理想**: 各sceneで **動画が1本**できる（`scenes/sceneXX/video.mp4`）

## Inputs / Outputs

### Input

- `topic`（必須）
- 上流成果物（コマンド内で生成する想定）
  - `research.md`
  - `story.md`（questionを含む）

### Output (run root)

- `output/<topic>_<timestamp>/`
  - `state.txt`（追記型）
  - `research.md`
  - `story.md`
  - `series_plan.md`（sceneごとの question を抜き出した計画）
  - `scenes/sceneXX/`（sceneごとの成果物）

### Output (per scene)

- `output/<topic>_<timestamp>/scenes/sceneXX/`
  - `evidence.md`（question→answer の根拠集約）
  - `script.md`（30–60秒のQ&A用ナレーション＋指示）
  - `video_manifest.md`（素材生成/選定/結合の指示）
  - `assets/**`（画像/動画/音声）
  - `video.mp4`（最終）
  - `logs/**`（任意）

## Provider assumptions

- Image: Google Nano Banana Pro（Gemini Image）
- Video: Google Veo 3.1
- TTS: ElevenLabs

（※ プロバイダ差し替え可能な設計を維持）

## Non-goals (for now)

- 「現実寄り / 抽象寄り」など **映像表現の方針の最終決定**は、実装直前に再確認する
- 高度なプロンプト最適化（Prompt Optimizerの反復）は後続タスク
- 自動字幕（SRT）や高度な編集（複数カット/テロップ演出）は後続タスク

## Open questions (defer)

- sceneのビジュアル方針（現実/抽象、図解/再現、人物の扱い）
- scene内を「1カットで30–60秒」か「複数カット合成」にするか
  - MVPは1カットを基本にし、必要なら複数カットへ拡張する想定

