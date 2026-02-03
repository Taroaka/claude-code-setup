# Design: scene_id 配賦（運用・テンプレ・指示）

## 変更点

- `workflow/research-template.yaml`
  - `scene_plan`（min_scene_count=20 / scenes[]）を追加
  - hooks に `scene_ids` を追加（同様に他項目も運用で付与）
- `docs/information-gathering.md`
  - Scene mapping の章を追加（ルール/期待出力）
- `.claude/agents/deep-researcher.md`
  - scene_plan 作成と scene_id 配賦の必須化
- `workflow/story-template.yaml`
  - sceneごとの `research_refs` を追加（traceability）

## 運用ルール（要点）

- scene_id は原則 1..20（最低20）
- 全体情報は opening/ending（例: 1, 19, 20）
- 途中ネタは該当 scene_id（複数可）

