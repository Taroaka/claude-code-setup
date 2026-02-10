# Design: split scene-production into three categories

## New categories
- `workflow/playbooks/scene/`
- `workflow/playbooks/image-generation/`
- `workflow/playbooks/video-generation/`

## Selector change
- natural language selector を 3カテゴリ入力から 5カテゴリ入力へ更新
- 曖昧指定時のみ不足カテゴリを確認
- 旧「シーン画像動画」一括指定は backward compatibility で受理

