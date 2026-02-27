# Requirements: Seedance (BytePlus ModelArk) Video Provider

## Goal

Enable generating videos via **ByteDance/BytePlus ModelArk** using the **Seedance** video generation API, alongside existing Kling-based video generation.

## User Story

- As a video-generation pipeline user, I want to set `scenes[].video_generation.tool` to a ByteDance/BytePlus option (e.g. `seedance`) so I can generate scene videos via the official ModelArk API with:
  - **no audio** by default
  - **reference images** (character/item) for consistency

## Non-Goals

- Replacing existing Kling/EvoLink video generation.
- Building a UI for authoring complex multi-image prompts; we only need a best-effort mapping from the manifest fields to the API payload.
- Implementing BytePlus File API upload (we use base64 `data:image/...;base64,...` URLs for images).

## Constraints / Safety

- Do not read or print secrets.
- Keep changes minimal and reversible; prefer env/CLI switches.
- Default to **no audio** unless explicitly enabled.

## Acceptance Criteria

- `scripts/generate-assets-from-manifest.py` supports a Seedance/ModelArk video tool name and generates an `.mp4` to `video_generation.output`.
- Local first/last-frame images are sent as base64 data URLs with explicit roles (`first_frame`, `last_frame`).
- `image_generation.references` can be used as video reference images (`role: reference_image`).
- Task polling works via the official retrieve endpoint until `status: succeeded` (or fails fast on terminal failure statuses).

