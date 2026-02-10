# Requirements: Video Tool Routing (Veo/Kling)

## Goal

- Allow the user to specify `veo` or `kling` for video generation.
- Use that choice to decide the video-generation branch of the workflow.

## In Scope

- Manifest: `scenes[].video_generation.tool` supports:
  - `google_veo_3_1`
  - `kling_3_0`
- Asset generation: `scripts/generate-assets-from-manifest.py` generates video for either tool.
- Scaffolding helpers: scripts that create manifests can accept `--video-tool veo|kling`.
- Update minimal docs/prompts so agents know how to set `video_generation.tool`.

## Out of Scope

- Changing image/TTS providers.
- Implementing provider-specific prompt tuning beyond existing prompts.
