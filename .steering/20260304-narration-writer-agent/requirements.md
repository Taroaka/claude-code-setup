# Narration Writer agent (requirements)

## Background

`audio.narration.text` は ElevenLabs へそのまま送られる「読み上げ原稿」である。
placeholder として `TODO: ...` を入れると、そのまま喋られて事故になる。

また、カット設計は「1カット=1ナレーション（メイン5–15秒、サブ3–15秒）」で進めたいが、
現状は `video_manifest.md` 内のナレーション原稿が未確定のまま素材生成に進めてしまい、
TTS/尺/タイムラインが後追いになりがちだった。

## Goals

- `audio.narration.text` を **必須の成果物**として扱い、未記入のまま生成に進めない
- placeholder は `""`（空）を基本とし、**未記入はエラーで検出**できるようにする
- ナレーション原稿を作成する専用エージェント（`narration-writer`）を追加する
- 生成フローに「音声→実秒→カット秒数/タイムライン確定（timestamp更新）」を組み込む
- `/toc-run` / `/toc-scene-series` / `/toc-immersive-ride` に適用する
  - ただし **`/toc-immersive-ride --experience cloud_island_walk` は対象外**

## Non-goals

- 音声の声色/演技の自動最適化
- 既存 `output/` 成果物の全自動改修
- 自動で cut を増減させる（分割判断は将来拡張）

