# Data Contracts (MVP)

本書は `todo.txt` の 6) Data contracts を具体化する。

## 1. State schema（ジョブ状態）

`docs/orchestration-and-ops.md` のマニフェストを最小化し、
**テキスト（key=value）で状態を管理**する。

状態ファイルはプロジェクトフォルダに置く：

```
output/<topic>_<timestamp>/state.txt
```

更新方式は **追記型**（最新のブロックが現在状態）。

```text
timestamp=ISO8601
job_id=JOB_YYYY-MM-DD_0001
topic=string
status=INIT|RESEARCH|STORY|SCRIPT|VIDEO|QA|DONE
gate.research_review=required|optional|skipped
gate.story_review=required|optional|skipped
gate.video_review=required|optional|skipped
artifact.research=output/<topic>_<timestamp>/research.md
artifact.story=output/<topic>_<timestamp>/story.md
artifact.script=output/<topic>_<timestamp>/script.md
artifact.video=output/<topic>_<timestamp>/video.mp4
---
```

対応テンプレート: `workflow/state-schema.txt`

---

## 2. Artifact paths（成果物パス）

標準パス:

```
output/<topic>_<timestamp>/
  research.md
  story.md
  script.md
  video.mp4
  video_manifest.md
  assets/
```

scene-series（Q&A動画を複数本）:

```
output/<topic>_<timestamp>/
  series_plan.md
  scenes/sceneXX/
    evidence.md
    script.md
    video_manifest.md
    assets/
    video.mp4
```

---

## 3. Output templates（最小テンプレ）

以下のテンプレートをMVPの出力契約とする。

- `workflow/research-template.yaml`
- `workflow/story-template.yaml`
- `workflow/script-template.yaml`

各テンプレートは `docs/information-gathering.md` / `docs/story-creation.md` /
`docs/script-creation.md` のスキーマから最小フィールドのみ抽出。
