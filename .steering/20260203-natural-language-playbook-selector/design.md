# Design: MD-only selector

## Structure
- `workflow/playbooks/research/*.md`
- `workflow/playbooks/script/*.md`
- `workflow/playbooks/scene-production/*.md`
- `workflow/playbooks/selectors/pipeline-selector-natural-language.md`

## Decision
- 各カテゴリは「1ファイル=1方式」
- selectorは入力の自然言語を方式ファイルへマップするルールのみ定義

