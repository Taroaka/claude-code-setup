# Design: Scene outline を asset brief として拡張

## 変更方針

- `workflow/scene-outline-template.yaml` を新設し、sceneごとに生成用の具体情報を持たせる。
- `workflow/playbooks/scene/scene-outline-from-story.md` を更新し、`research.md` の `facts/sources` と結び付けて埋める運用にする。
- 下流の playbook も `scene_outline` を入力前提として揃える（image/video）。
- `docs/data-contracts.md` に scene template を追加し、正式な出力契約として扱う。

## 追加する情報（scene単位）

- 根拠: `factual_anchors.fact_ids/source_ids`（不確実なら unverified を明示）
- 画作り: `setting/characters_present/props_set_pieces/action_beats`
- 一貫性: `camera/lighting_color/continuity`
- 生成指針: `prompt_guidance`（image/video の focus/negative/motion）
- 創作: `creative_inventions` に明示（セット装飾などの発明をラベル付け）
- 追加調査: `research_tasks`（欠けている具体を scene 単位で補う。evidence を残す）

## 期待する効果

- sceneごとの情報密度が上がり、画像/動画プロンプトが機械的に組み立てられる
- 未知トピックでも、researchの根拠とsceneの具体が繋がり、幻覚とブレを抑える
- 不足が出た場合に、scene単位で追加調査して埋め戻せる（生成前に解消）
