# Narration Writer agent (design)

## Contract

- `audio.narration.text` は **読み上げ原稿そのもの**（メタ情報やTODOを書かない）
- 原稿は **日本語**、1カット=1ナレーション
- 文体は、YouTubeを見る20代前後が無理なく入れる **平易で寄り添う話し言葉** を優先する
- 物語の深い設計、抽象テーマ、解釈の余地は **主に映像側** に置く
- ナレーションで設計を露骨に説明しない
- ただし終盤の学び/余韻パートでは、満足感のために軽い言語化を許容する
- 尺制約:
  - main: 5–15秒
  - sub: 3–15秒
- 15秒を超えそうな場合:
  - 原稿を短くする、または cut 分割を提案（自動分割は非対応）

## Pipeline integration

### 新しい責務分割

- `immersive-scriptwriter` / `scene-scriptwriter`:
  - `audio.narration` ブロック（tool/output/normalize_to_scene_duration）を用意
  - `text` は **空文字**（未記入）で残す
- `narration-writer`:
  - story/script と cut の意図から `audio.narration.text` を埋める
  - 台本（`script.md`）側にも同等の原稿を反映（将来の手直し用）

### 生成（素材）側

1) audio-only で TTS を生成
2) 実秒から `video_generation.duration_seconds` と `scenes[].timestamp` を同期
3) 画像/動画生成へ進む（音声は `--skip-audio`）

## Data locations

- 役割定義: `.claude/agents/narration-writer.md`
- 仕様正本:
  - `docs/implementation/agent-roles-and-prompts.md`
  - `docs/implementation/langgraph-topology.md`
  - `docs/implementation/video-integration.md`
