# Multi-agent Immersive Narration Playbook (ToC)

目的: `/toc-immersive-ride` の `video_manifest.md` について、cuts（3〜5）に対応する
**ナレーション原稿（`audio.narration.text`）**を衝突なく並列で作成する。

## 原則

- `audio.narration.text` は TTS にそのまま送られる。`TODO:` などのメタ情報を書かない。
- 共有ファイル（`video_manifest.md`）は **同時編集しない**（single-writer で統合）。
- 並列化は「scene別 scratch」→「1人がマージ」で実現する。

## ファイル構成（run dir）

`output/<topic>_<timestamp>_immersive/`
- `video_manifest.md`（正本 / single-writer が更新）
- `state.txt`（必要なら single-writer が更新）
- `scratch/narration/sceneXX.yaml`（scene担当が編集 / scene単位で競合しない）

## Phase 0: Prepare scratch（直列）

single-writer が scratch 雛形を作る:

```bash
python scripts/ai/toc-immersive-narration-multiagent.py \
  --run-dir "output/<topic>_<timestamp>_immersive" \
  --min-cuts 3
```

## Phase 1: Per-scene narration drafting（並列）

scene担当者は、自分の scene の scratch だけ編集して原稿を入れる:

- 例: `scratch/narration/scene02.yaml`
  - `cuts[].narration_text` に **読み上げ原稿のみ**を書く（日本語）
  - 1カット=1ナレーション
  - main=5–15秒、sub=3–15秒を目安に短く

## Phase 2: Merge to manifest（直列）

single-writer が scratch を manifest へ統合:

```bash
python scripts/ai/merge-immersive-narration.py \
  --run-dir "output/<topic>_<timestamp>_immersive"
```

## Phase 3: Next（ユーザーが起動）

原稿が埋まったら、音声→尺同期→映像生成へ進む:

```bash
scripts/toc-immersive-ride-generate.sh --run-dir "output/<topic>_<timestamp>_immersive"
```

