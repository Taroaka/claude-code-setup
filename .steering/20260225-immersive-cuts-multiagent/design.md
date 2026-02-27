# Design: Immersive cuts multi-agent (scratch → merge)

## Overview

1) `scripts/ai/toc-immersive-cuts-multiagent.py` が run dir を指定して scratch 雛形を作る  
2) multi-agent（tmux）で scene担当者が `scratch/cuts/sceneXX.yaml` を編集し cuts を設計する  
3) single-writer が `scripts/ai/merge-immersive-cuts.py` で `video_manifest.md` に統合する  
4) 統合後、ユーザーへ「次に起動する」コマンド（例: `scripts/toc-immersive-ride-generate.sh`）を案内する

## Files

- Input（single-writer）:
  - `<run_dir>/video_manifest.md`
- Input（per-scene, parallel-safe）:
  - `<run_dir>/scratch/cuts/sceneXX.yaml`
- Output（single-writer）:
  - `<run_dir>/video_manifest.md`（`scenes[].cuts` を更新）
  - `<run_dir>/state.txt`（任意: next step を追記）

## Scratch format (sceneXX.yaml)

- 最低限:
  - `scene_id: <int>`
  - `cuts:`
    - `cut_id: <int>`
      `image_generation: { tool, prompt, output, character_ids, object_ids, ... }`
- `output` は既定で `assets/scenes/scene{scene_id:02d}_cut{cut_id:02d}.png`

## Merge rules

- 対象 scene:
  - character reference 用の scene（0, 100, 101...）は除外
  - 既に `cuts` を持つ scene は上書きしない（`--force` 指定時のみ上書き）
- `sceneXX.yaml` が存在しない scene はスキップ
- cuts 数は 3〜5 を推奨（`--min-cuts/--max-cuts` で検証）

## Safety

- マージ前に manifest をバックアップ（`video_manifest.md.bak`）を作る（`--no-backup` で無効化）
- YAML parse/validation が失敗した場合は何も書き換えない

