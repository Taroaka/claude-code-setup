# System Architecture (MVP)

This document captures the architecture decisions for the MVP and the path to
future cloud deployment. It corresponds to todo item 1 in `todo.txt`.

## Scope and assumptions

- Orchestration uses LangGraph.
- MVP is single-user, local-first.
- Input: story title. Output: artifacts under `output/<topic>_<timestamp>/`.
- External model providers are optional; mock providers are acceptable for MVP.

## Decision summary

| Area | Decision | Rationale |
| --- | --- | --- |
| Deployment mode | Local-only MVP | Fast iteration, zero infra |
| Execution model | Single-node orchestrator + in-process workers | Lowest complexity for MVP |
| Storage | Filesystem object store + PostgreSQL metadata DB | Durable metadata |
| Job queue | In-process async queue | Simple and sufficient for MVP |
| State management | Append-only `state.txt` in project folder (no DB checkpoints) | Human-readable recovery |
| Providers | LLM via LangChain; image/video/TTS TBD (pluggable) | Avoid vendor lock-in |
| API boundary | Claude Code entrypoint (slash command) | Keep surface area small |

## Component diagram

```mermaid
graph TD
  CC[Claude Code Slash Command] --> ORCH[LangGraph Orchestrator]
  ORCH --> QUEUE[In-process Job Queue]
  QUEUE --> WORKERS[Workers]
  WORKERS --> PROVIDERS[Image/Video/TTS/LLM Providers]
  ORCH --> META[Metadata DB (PostgreSQL)]
  ORCH --> STATE[State File (state.txt)]
  PROVIDERS --> OBJ[Object Store (filesystem)]
  OBJ --> ARTIFACTS[Artifacts: research/story/script/video]
```

## Deployment mode

- MVP: local-only, Claude Codeで起動（slash command）。
- Future: containerized deployment with dev/staging/prod environments.

## Execution model

- Single-node orchestrator runs the LangGraph.
- Long-running tasks executed via in-process worker pool (async + process/thread).
- Concurrency default: 2 workers; configurable via `config/system.yaml`.
- Parallelism policy (MVP):
  - Core flow (RESEARCH → STORY → SCRIPT → REVIEW) is sequential.
  - Parallelizable points are limited to:
    - Within a single approved scene: generate assets (image, TTS, video) in parallel.
    - After a scene is approved: start that scene's asset generation while the next scene is being drafted/reviewed.

## Storage strategy

- Object storage (artifacts): filesystem at `output/`.
- Metadata DB: PostgreSQL (local or managed).
- Paths are configured in `config/system.yaml`.

## Job queue / executor

- In-process queue with worker pool.
- Tasks are stage-scoped (RESEARCH, STORY, SCRIPT, VIDEO, QA).
- Retry logic is handled at the LangGraph edge level (future task).

## Task granularity (MVP)

- Base unit is a stage task aligned to LangGraph nodes:
  - `RESEARCH` → produces `research.md`
  - `STORY` → produces `story.md`
  - `SCRIPT` → produces `script.md` (scene plan + narration text)
  - `VIDEO` → produces assets + `video.mp4`
  - `QA` → produces review/score + pass/fail
- Scene-level tasks exist only inside `SCRIPT` and `VIDEO`:
  - `SCRIPT` subtask: draft one scene from the approved scene plan.
  - `VIDEO` subtask: generate assets for an approved scene (image, TTS, clip).
- Asset-level tasks exist only inside `VIDEO`:
  - Image, TTS, and clip generation are independent per approved scene.
- Granularity principles:
  - Keep core flow sequential and gate-driven.
  - Only split tasks where outputs are independently verifiable.
  - Retries should target the smallest failing unit (scene or asset), not the whole job.

## State management

- 状態は `output/<topic>_<timestamp>/state.txt` に **追記型** で記録する。
- 最新ブロックが現在状態、過去ブロックをコピーして擬似的にロールバック可能。

## Model/providers

- Provider interfaces for image, video, TTS, and LLM.
- LLM integration uses LangChain.
- Image/video/TTS providers are TBD (keep pluggable, use mock locally).
- Swap providers via configuration without changing orchestration logic.

## API boundaries / module ownership

- MVP: Claude Code の呼び出しが起点（slash command）。
- CLIやHTTPサーバは対象外（将来拡張）。
- Proposed internal modules:
  - `app/orchestrator`: LangGraph topology and run logic
  - `app/providers`: image/video/tts/llm adapters
  - `app/storage`: object store + metadata DB access
  - `app/queue`: in-process queue + worker pool
  - `app/cli`: CLI entrypoint

## Config source of truth

- `config/system.yaml` defines the defaults for the MVP.
- Environment overrides are expected in later tasks.

## Open questions

- Which cloud provider to standardize on (AWS/GCP/etc.)?
- Which production providers for image/video/TTS?
- Preferred trade-off: cost vs quality vs latency?
