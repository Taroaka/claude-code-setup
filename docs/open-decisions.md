# Open Decisions

本書は、未確定事項（TBD）を集約する。

## Providers
- image: Google Nano Banana Pro（Gemini Image / `gemini-3-pro-image-preview`）
- video: Kling 3.0（default。`video_generation.tool: kling_3_0`）
- video (omni): Kling 3.0 Omni（`video_generation.tool: kling_3_0_omni`）
- video (alt): Google Veo 3.1（`video_generation.tool: google_veo_3_1`）
- TTS: ElevenLabs（voice/model/output_format は運用で確定）
- LLM provider is LangChain (API-based)
- 候補整理/調査リスト: `docs/video-production-research.md`

## Claude Code entrypoint
- `/toc-run` の実装方法（Claude Code側の具体設定）

## Rendering details
- 字幕（SRT）の生成方法
- BGM/SFX の扱い（内製/生成、音量基準）

## Data/Logging
- `orchestration_manifest.md` と `run_report.md` の正本（ファイル/DBの役割分担）
