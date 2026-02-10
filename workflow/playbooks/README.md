# Playbooks (Natural Language Selection)

このディレクトリは、パイプラインを構成する方式定義を置く。

5ステップ（推奨）:
- `workflow/playbooks/research/`
- `workflow/playbooks/script/`
- `workflow/playbooks/scene/`
- `workflow/playbooks/image-generation/`
- `workflow/playbooks/video-generation/`
- `workflow/playbooks/selectors/`

運用:
- ユーザーは自然言語で「やり方×5」を指定する
- selector は各カテゴリから1つずつ選ぶ
- 方式は `*.md` を増やすだけで拡張できる

selectorルール:
- `workflow/playbooks/selectors/pipeline-selector-natural-language.md`

互換:
- 旧カテゴリ `workflow/playbooks/scene-production/` は互換目的で残す
- 新規運用は `scene` / `image-generation` / `video-generation` の分離を優先する
