# Scene Method: Scene Outline From Story

## Use when
- `story.md` から scene責務を先に確定し、後段の画像/動画生成を安定させたいとき

## Scope
- この方式は **scene定義のみ** を担当する
- 画像生成・動画生成は別カテゴリ方式で処理する

## Steps
1. `story.md` の `script.scenes[]` を読み、sceneごとの目的を固定する
2. 各sceneに `goal/conflict/stakes/transition_in/transition_out` を付与する
3. `research.md` の `facts/hooks` を参照し、各sceneに根拠（`fact_ids/source_ids`）を紐づける
4. 画像/動画生成に必要な情報を scene単位で埋める（setting/camera/continuity/prompt_guidance）
5. scene間の連続性チェック（時系列・視点・感情・画の繋がり）を実施する
6. 必須フィールドが `tbd` の場合は `research_tasks` を起票し、evidence を作って埋める（生成前に解消）

## Output contract
- scene定義ファイル（`scene_id`, `phase`, `goal`, `transition_in`, `transition_out`）
- **Asset brief**（未知トピックでも生成できるだけの情報量）
  - `factual_anchors.fact_ids/source_ids`（根拠）
  - `setting/characters_present/props_set_pieces/action_beats`（画作りに必要な具体）
  - `camera/lighting_color/continuity`（一貫性）
  - `prompt_guidance`（image/videoの指針、禁止、creative_inventionsの明示）
- 任意: sceneごとの evidence（追加調査が必要な場合）
  - `output/<topic>_<timestamp>/scenes/sceneXX/evidence.md`
  - template: `workflow/scene-evidence-template.md`

Template:
- `workflow/scene-outline-template.yaml`
