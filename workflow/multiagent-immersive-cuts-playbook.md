# Multi-agent Immersive Cuts Playbook (ToC)

目的: `/toc-immersive-ride` の `video_manifest.md` を、scene2+ について **cuts（3〜5）** に分割しつつ、衝突なく並列で設計する。

## 原則

- 共有ファイル（`video_manifest.md`）は **同時編集しない**（single-writer で統合）。
- 並列化は「scene別 scratch」→「1人がマージ」で実現する。

## ファイル構成（run dir）

`output/<topic>_<timestamp>_immersive/`
- `video_manifest.md`（正本 / single-writer が更新）
- `state.txt`（必要なら single-writer が更新）
- `scratch/cuts/sceneXX.yaml`（scene担当が編集 / scene単位で競合しない）

## Phase 0: Prepare scratch（直列）

single-writer が scratch 雛形を作る:

```bash
python scripts/ai/toc-immersive-cuts-multiagent.py \
  --run-dir "output/<topic>_<timestamp>_immersive" \
  --min-cuts 3 --max-cuts 5
```

## Phase 1: Per-scene cuts design（並列）

scene担当者は、自分の scene の scratch だけ編集して cuts を決める:

- 例: `scratch/cuts/scene02.yaml`
  - cuts 数: 3〜5
  - `image_generation.prompt` は cut ごとに目的（構図/アクション/役割）を変える
  - `image_generation.output` は衝突しない命名にする（推奨: `assets/scenes/scene02_cut01.png`）

## Phase 2: Merge to manifest（直列）

single-writer が scratch を manifest へ統合:

```bash
python scripts/ai/merge-immersive-cuts.py \
  --run-dir "output/<topic>_<timestamp>_immersive"
```

## Phase 3: Next（ユーザーが起動）

統合が終わったら、次を起動して生成へ進む:

```bash
scripts/toc-immersive-ride-generate.sh --run-dir "output/<topic>_<timestamp>_immersive"
```

