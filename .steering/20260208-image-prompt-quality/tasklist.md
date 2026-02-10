# Tasklist: 画像生成プロンプト品質の底上げ

## 1) Deep research（調査→正本化）

- [x] 外部ドキュメント/一次情報（Gemini/Imagen の prompt guide 等）を収集し、要点を抽出する
- [x] `docs/implementation/image-prompting.md` を作成（構造化テンプレ + 具体例 + チェックリスト）

## 2) テンプレ/エージェント指示（A: 上流で構造化）

- [x] `workflow/immersive-ride-video-manifest-template.md` を更新（GLOBAL→SCENE の流れ + 具体例）
- [x] `.claude/agents/immersive-scriptwriter.md` を更新（prompt構造の強制 + 参照画像運用の明文化）
- [x] `workflow/video-manifest-template.md` / `workflow/scene-video-manifest-template.md` も必要なら同様に更新

## 3) 生成スクリプト改善（B: 下流で assets を自動注入）

- [x] `scripts/generate-assets-from-manifest.py` で `assets.character_bible/style_guide` を読み取る（`--apply-asset-guides`）
- [x] `references` 自動マージ（character/style の ref を scene ref に追加）
- [x] `fixed_prompts` / `forbidden` を prompt に反映（見出しがある場合は該当セクションへ注入）
- [x] 最終的に API に送る prompt をログ保存（`logs/providers/sceneN_image_prompt.txt` / `sceneN_video_prompt.txt`）

## 4) 検証

- [x] unit test を追加（assets 解析 + prompt 組み立ての期待）
- [x] `python -m compileall .`（最低限）
