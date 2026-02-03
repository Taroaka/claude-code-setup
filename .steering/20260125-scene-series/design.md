# Scene-Series Slash Command: Design

## Overview

このコマンドは「topic → research → story → sceneごとのQ&A動画」を作る。

既存の `/toc-run`（topic起点の全体フロー）とは別に、**scene単位の派生動画（複数本）**を出すための入口。

## High-level flow

```text
TOPIC
  → RESEARCH (deep-researcher)
  → STORY (director)
  → SERIES_PLAN (extract questions)
  → for each scene:
       EVIDENCE (use research first; web fallback)
       SCENE_SCRIPT (30–60s)
       SCENE_MANIFEST
       GENERATE_ASSETS (image/video/tts)
       RENDER (sceneXX/video.mp4)
       QA (optional/manual-first)
```

## Artifacts and contracts

### `series_plan.md` (run root)

目的: 「何を何本作るか」を固定し、以降の工程の入力を安定させる。

最低限:
- scene_id
- main_text
- sub_text (question)
- target_seconds (30–60)
- notes (optional)

### `scenes/sceneXX/evidence.md`

目的: sceneの主張がどこから来たかを追跡可能にする。

最低限:
- question
- answer (short)
- evidence bullets (3–7)
- sources (URL/出典 + メモ)
- gaps (不足があれば)

### `scenes/sceneXX/script.md`

目的: 30–60秒で「問い→答え→根拠→締め」を成立させる制作台本。

最低限:
- narration（音声原稿）
- on-screen text（任意）
- pacing（秒割りはラフでOK）

### `scenes/sceneXX/video_manifest.md`

目的: 既存の生成/結合スクリプトで処理できるようにする（契約の中心）。

方針:
- sceneXX配下に `assets/` を置く（scene間で衝突しない）
- 30–60秒を **Veoの制約（4/6/8秒）に合わせて分割生成→結合/trim** するのは生成スクリプト側で吸収

## Evidence strategy

### First: reuse `research.md`

- question に対する答えの候補を `research.md` から抽出
- 根拠が足りる場合は、追加調査しない（コスト/時間削減）

### Fallback: targeted web research

- 不足時のみ、question を中心に追加調査（テキストベース前提）
- 出力は `scenes/sceneXX/evidence.md` に閉じる
  - run全体の `research.md` に追記するかは後で決める（現段階ではscene閉じでOK）

## Concurrency / ordering

- run全体は直列（RESEARCH→STORY→PLAN）
- sceneは **並列化可能**（EVIDENCE→SCRIPT→MANIFEST→ASSETS→RENDER）
  - ただしMVPではまず直列でよい（失敗時の原因切り分け優先）

## State tracking (`state.txt`)

run root の `state.txt` に追記:

- `runtime.stage=research|story|series_plan|scene_loop|done`
- `runtime.scene.<id>.status=planned|evidence|script|manifest|assets|rendered|failed`
- `runtime.scene.<id>.attempts=<n>`

## CLI / flags (proposed)

- `--dry-run`:
  - 外部API（image/video/tts）を呼ばない
  - ただし `series_plan.md` と per-scene の雛形までは作る
- `--min-seconds 30 --max-seconds 60`:
  - scene script の目標尺
- `--scene-ids 1,3,5`:
  - 部分実行/再実行のため

## Deferred decision: visual style (現実/抽象)

- sceneの `image_prompt` / `motion_prompt` の「現実寄り / 抽象寄り」は実装直前に再確認する
- MVPは **プロンプトをプレースホルダ**にして、後で切り替え可能な構造を優先

