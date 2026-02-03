# Scene-Series Slash Command: Tasklist

## 1) Spec / docs

- [ ] コマンド名を確定（例: `/toc-scene-series`）
- [ ] `.claude/commands/toc/<command>.md` を追加（入力/出力/オプション/注意）
- [ ] `docs/implementation/` に正本を昇華（まずは `.steering` で合意→後で移植）
- [ ] `docs/README.md` にリンク追加

## 2) New agent roles (Claude Code)

- [ ] `series-planner`（story/script → question plan）
- [ ] `scene-evidence-researcher`（question → evidence）
- [ ] `scene-scriptwriter`（evidence → 30–60s script）

※ 既存:
- `deep-researcher`（topic → research）
- `director`（research → story）

## 3) Templates / contracts

- [ ] `workflow/series-plan-template.yaml`
- [ ] `workflow/scene-evidence-template.md`
- [ ] `workflow/scene-script-template.yaml`（or md）
- [ ] `workflow/scene-video-manifest-template.md`（単一scene前提）

## 4) Implementation (runner)

- [ ] `scripts/toc-scene-series.py`（雛形生成 + 再実行）
  - [ ] run root 作成（`output/<topic>_<timestamp>/`）
  - [ ] `series_plan.md` 生成
  - [ ] `scenes/sceneXX/` 雛形生成
  - [ ] `--scene-ids` 部分実行
  - [ ] `--dry-run` でAPI呼び出しスキップ
- [ ] 生成実行は既存スクリプトを利用
  - `scripts/generate-assets-from-manifest.py`
  - `scripts/build-clip-lists.py`
  - `scripts/render-video.sh`

## 5) Validation

- [ ] dry-run でファイル構成が揃うことを確認
- [ ] 1 sceneだけ生成して E2E（manifest→assets→render）確認

## 6) Deferred (after reconfirm)

- [ ] prompt方針（現実/抽象）を決める
- [ ] sceneを「1カット」か「複数カット合成」へ拡張するか検討

