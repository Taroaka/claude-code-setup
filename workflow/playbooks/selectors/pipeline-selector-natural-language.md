# Pipeline Selector (Natural Language)

このファイルは、ユーザーの自然言語指定から 5カテゴリの方式を 1つずつ選ぶための運用ルール。

## Input format
- ユーザーが自然言語で以下5つを指定する
  - 調査方法
  - 台本の作り方
  - シーン設計方法
  - 画像生成方法
  - 動画生成方法
  - （任意）動画モデル（例: veo / kling）

例:
- 「調査は原典優先、台本は英雄譚ビート先行、シーンはstory由来分割、画像は参照一括、動画はfirst-last-frame連結で」

## Selection rule
1. `workflow/playbooks/research/` から 1件選ぶ
2. `workflow/playbooks/script/` から 1件選ぶ
3. `workflow/playbooks/scene/` から 1件選ぶ
4. `workflow/playbooks/image-generation/` から 1件選ぶ
5. `workflow/playbooks/video-generation/` から 1件選ぶ

## Matching policy
- IDは不要。自然言語の意図を最短でファイル名にマッピングする
- 推薦ロジックは持たない（ユーザー指定を優先）
- 曖昧な場合のみ、足りないカテゴリを 1問で確認する

### Video model note
- ユーザーが `veo` / `kling` を指定した場合は、playbook選択に加えて `video_manifest.md` の
  `scenes[].video_generation.tool` も一致させる
  - `veo` → `google_veo_3_1`
  - `kling` → `kling_3_0`

## Output format
- 選択結果を5行で返す:
  - `research: <path>`
  - `script: <path>`
  - `scene: <path>`
  - `image-generation: <path>`
  - `video-generation: <path>`

## Backward compatibility
- ユーザーが「シーン画像動画をまとめて指定」した場合は、次の 3件を同時に選ぶ:
  - `scene`
  - `image-generation`
  - `video-generation`
