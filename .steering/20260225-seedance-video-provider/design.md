# Design: Seedance (BytePlus ModelArk) Video Provider

## Overview

Add a new provider client `toc/providers/seedance.py` that talks to BytePlus ModelArk “contents generation tasks” endpoints for Seedance video generation:

- Submit a task via `POST /contents/generations/tasks`
- Poll task status via `GET /contents/generations/tasks/{id}`
- Download the resulting `content.video_url` to the manifest output path

Then wire `scripts/generate-assets-from-manifest.py` so `scenes[].video_generation.tool` can be set to Seedance-related aliases.

## API Mapping (ModelArk)

- Create task:
  - `POST {ARK_API_BASE}/contents/generations/tasks`
  - Response: `{ "id": "cgt-..." }`
- Retrieve task:
  - `GET {ARK_API_BASE}/contents/generations/tasks/{id}`
  - Response includes:
    - `status` (e.g. `succeeded`)
    - `content.video_url` (download URL)

## Payload Mapping (manifest → API)

- Prompt: `Scene.video_motion_prompt` + `Scene.image_prompt` → `content: [{type:"text", text: ...}]`
- First frame:
  - `video_generation.first_frame`/`input_image` → `content` item with `role: "first_frame"`
- Last frame (opt-in):
  - `video_generation.last_frame` (when `--enable-last-frame`) → `role: "last_frame"`
- Reference images:
  - `image_generation.references[]` (after asset-guide merging) → `role: "reference_image"`

Images are encoded as `data:image/<fmt>;base64,<...>` so we do not need to integrate the File API.

## Configuration

Environment variables (and equivalent CLI flags):

- `ARK_API_KEY` (fallback: `SEADREAM_API_KEY`)
- `ARK_API_BASE` (fallback: `SEADREAM_API_BASE`)
- Model selection (auto-picked by I2V vs T2V):
  - `ARK_SEEDANCE_I2V_MODEL`
  - `ARK_SEEDANCE_T2V_MODEL`
- Optional payload override:
  - `ARK_EXTRA_JSON` (merged into request payload)

## Routing / Tool Names

Supported `video_generation.tool` values (normalized):

- `seedance`, `byteplus_seedance`, `bytedance_seedance`, `ark_seedance`
- `seadream_video`, `seedream_video`, `see_dream` (aliases for “ByteDance see dream” wording)

## Safety Defaults

- `generate_audio`: false (unless explicitly enabled by `--ark-generate-audio` or via `ARK_EXTRA_JSON`)
- `watermark`: false

