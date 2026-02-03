# Multi-agent Scene-Series Playbook (ToC)

目的: `topic → research → story/script → scenes/sceneXX/` を **衝突なく** 並列で進める。

## 原則

- 共有ファイル（`research.md`, `story.md` など）は **同時編集しない**（RACE-001）。
- 並列化は「各自専用scratch」→「1人が統合（single-writer）」で実現する。
- scene生成は `scenes/sceneXX/` を単位に並列化する（競合しない）。

## ファイル構成（run dir）

`output/<topic>_<timestamp>/`
- `research.md`（統合成果物 / single-writer）
- `story.md`（統合成果物 / single-writer）
- `state.txt`（必要なら single-writer で更新）
- `scratch/ashigaruN/`
  - `research_notes.md`（各自の調査メモ / ashigaruN専用）
  - `story_notes.md`（各自の台本/scene案 / ashigaruN専用）
- `scenes/sceneXX/`（scene別成果物 / scene担当のみ編集）

## Phase 1: Research（並列 → 統合）

- ashigaru1..N: それぞれ別観点で調査し、`scratch/ashigaruN/research_notes.md` に書く
- single-writer（1名）: 全scratchを読んで `research.md` に統合する

## Phase 2: Story/Script（並列 → 統合）

- ashigaru1..N: `scratch/ashigaruN/story_notes.md` に scene案やQ&A案を書く
- single-writer（1名）: `story.md`（または `script.md`）に統合する

## Phase 3: Scaffold scenes（直列）

single-writer が `scripts/toc-scene-series.py` で雛形を作る:

```bash
python scripts/toc-scene-series.py "topic" --run-dir "output/<topic>_<timestamp>" --dry-run
```

## Phase 4: Scene production（並列）

- ashigaru: 自分の担当sceneの `scenes/sceneXX/` だけ編集して完成させる
  - `evidence.md`
  - `script.md`
  - `video_manifest.md`

## Phase 5: Summary（直列）

single-writer が全sceneを読み、サマリ（例: `multiagent_summary.md`）を作る。

