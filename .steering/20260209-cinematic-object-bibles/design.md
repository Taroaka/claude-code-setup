# Design: object/setpiece bible（映画での役割 + 映像情報 + ショー性）を manifest-first で注入する

## 方針

### A) 正本は manifest（`video_manifest.md`）に置く

- `/toc-immersive-ride` の `video_manifest.md` が下流生成の唯一の入力なので、bible もここに置く（manifest-first）。
- ただし “読む側” の理解を助ける正本は `docs/implementation/asset-bibles.md` に置き、スキーマ/例/設計観点を明文化する。

### B) “映画での役割” と “映像から与える情報” を設計として保持する

アイテム/舞台装置は、メイン筋に直接関係しないディテールでも映像の魅力を作る。
そのため object ごとに以下を設計する:

- **Role in film**: 境界/誘惑/贈与/代償/啓示/帰還の証…など、映画の中で担う機能
- **Visual takeaways**: 観客が映像から理解すべき情報（言語化は設計に残し、画面内文字で説明しない）
- **Spectacle details**: メイン筋に無関係でも“ワクワク”を作る見せ場（ショー/仕掛け/現象）
- **Fixed prompts**: 生成に直接使う、不変条件（材質/構造/ルール/禁止）を短文で

これらを “都度の思いつき” ではなく、bible として固定し `--apply-asset-guides` で scene prompt に注入する。

## データ契約（public interface）

### `assets.object_bible[]`

必須（生成スクリプトが読む）:
- `object_id`
- `kind`（setpiece|artifact|phenomenon）
- `reference_images[]`（非空）
- `fixed_prompts[]`（非空）

強く推奨（映像設計の質を上げる）:
- `cinematic.role`
- `cinematic.visual_takeaways[]`
- `cinematic.spectacle_details[]`

### `scenes[].image_generation.object_ids`

- scene に映す object を ID で宣言（混ざり防止）
- B-roll も `object_ids: []` を明示（ゲートで強制可能）

## 実装（生成スクリプト）

`scripts/generate-assets-from-manifest.py`:

- `assets.object_bible` をパースし、`AssetGuides.object_bible` に保持
- `scenes[].image_generation.object_ids` をパースし、scene に保持
- `--apply-asset-guides` の適用時:
  - `object_ids` に応じて `reference_images` を `references` にマージ
  - `fixed_prompts` と cinematic 情報を `[PROPS / SETPIECES]` に注入
  - reference scene（`output` が `reference_images` に一致する scene）は self-reference を除外しつつ active 扱い
- ゲート:
  - `--require-object-ids`（object_bible がある場合、各 scene に `object_ids` を必須化）
  - `--require-object-reference-scenes`（reference_images の各パスが、どこかの scene output になっていること）

## テンプレ/運用

- `workflow/immersive-ride-video-manifest-template.md` / `workflow/immersive-cloud-island-walk-video-manifest-template.md`
  - `assets.object_bible`（空配列 + 例）を追加
  - すべての scene に `object_ids: []` を追加
- `scripts/toc-immersive-ride.py`
  - scaffold で `assets/objects/` を作る
- `scripts/toc-immersive-ride-generate.sh`
  - `--require-object-ids --require-object-reference-scenes` を常時 ON（品質ゲート）

## ドキュメント（正本）

- `docs/implementation/asset-bibles.md`:
  - スキーマ、reference scene 運用、設計観点（役割/映像情報/ショー性）、浦島太郎例
- `docs/implementation/image-prompting.md`:
  - 見出し順に `[PROPS / SETPIECES]` を追加し、書き分けを明記

