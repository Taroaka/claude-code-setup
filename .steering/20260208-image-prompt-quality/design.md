# Design: Prompt “全体→個別”の構造化 + 共通部の自動注入

## 方針（A + B を両立）

### A) 上流で prompt を構造化（即効性）

- `video_manifest.md` の `scenes[].image_generation.prompt` を「見出し + 順序固定」で書く。
- 目的は、下流（画像生成スクリプト/エージェント）が **優先順位と不変条件**を取りこぼさないこと。

推奨ブロック（順序固定）:

1. `GLOBAL / INVARIANTS`（全scene共通の不変条件）
2. `CHARACTERS`（人物・参照一致）
3. `SCENE`（場面固有の描写）
4. `CONTINUITY`（前後接続）
5. `AVOID`（禁止/地雷）

### B) 下流で assets を読み、共通部を自動注入（運用の再現性）

- 現状 `assets.character_bible` / `assets.style_guide` は“メモ”になっているため、
  生成スクリプト（`scripts/generate-assets-from-manifest.py`）側で以下を行う:
  - `assets.style_guide.visual_style` / `forbidden[]` を prompt に反映（prefix / avoid）
  - `assets.character_bible[].fixed_prompts[]` を prompt に反映（invariants）
  - `assets.character_bible[].reference_images[]` / `assets.style_guide.reference_images[]` を `references` に自動マージ
- ただし **破壊的変更を避ける**ため、まずは opt-in（例: `--apply-asset-guides`）で導入し、`/toc-immersive-ride` の生成シェルがそれを有効化する。

## 成果物（正本の置き場所）

- 深掘りした prompt 指針・具体例: `docs/implementation/image-prompting.md`
  - 理由: システムの根幹（品質/再現性）で、実装やテンプレを横断するため `docs/implementation/` が妥当。
- 運用手順（画像生成方式）との接続: `workflow/playbooks/image-generation/reference-consistent-batch.md` から参照
  - 理由: “いつ使うか/どう組み立てるか”の運用は playbook が担当するため。

## 互換性 / リスク

- 既存 manifest は引き続き動く（未指定の `assets` を必須にしない）。
- `generate-assets-from-manifest.py` の YAML パースは現状簡易実装なので、
  B の実装では PyYAML（`yaml.safe_load`）への切り替え or 併用を検討する。
- 自動注入により prompt が長くなるため、モデルの解釈が変わる可能性がある。
  - 対策: “共通部は短く固定、scene差分を優先”のテンプレを用意し、ログに最終promptを保存する。

