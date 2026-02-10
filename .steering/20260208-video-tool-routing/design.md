# Design: Video Tool Routing (Veo/Kling)

## Overview

Routing is driven by `video_manifest.md`:

- `scenes[].video_generation.tool=google_veo_3_1` -> Veo branch
- `scenes[].video_generation.tool=kling_3_0` -> Kling branch

Scaffolding scripts accept `--video-tool veo|kling` and write the corresponding tool value into the manifest.

## Implementation Points

- `scripts/generate-assets-from-manifest.py`
  - Detect whether any scene needs Kling video generation.
  - Configure a `KlingClient` using `KLING_*` env (and CLI overrides).
  - Branch per-scene video generation based on normalized `video_generation.tool`.
- `.claude/agents/immersive-scriptwriter.md`
  - Teach the agent to set `video_generation.tool` based on user instruction.

## Compatibility

- Existing manifests that use `google_veo_3_1` continue working unchanged.
- New tool value `kling_3_0` is additive.
