# BytePlus ModelArk: Seedance（動画生成）

## 概要

ToC の `scripts/generate-assets-from-manifest.py` は、ByteDance/BytePlus の ModelArk（Ark API）経由で **Seedance** の動画生成に対応している。

- タスク作成: `POST /contents/generations/tasks`
- タスク取得: `GET /contents/generations/tasks/{id}`
- 完了後: `content.video_url` をダウンロードして `video_generation.output` に保存

## 使い方（manifest）

`video_generation.tool` に `seedance` を指定する。

```yaml
video_generation:
  tool: "seedance"
  input_image: "assets/scenes/scene01_base.png"   # first_frame として送る
  motion_prompt: "カメラはゆっくりドリーイン。髪が風で揺れる。"
  output: "assets/scenes/scene01.mp4"
```

### 参照画像（キャラ/アイテム一貫性）

この実装では **`image_generation.references[]`** を Seedance の `reference_image` として送る（`role: "reference_image"`）。

```yaml
image_generation:
  references:
    - "assets/characters/protagonist_refstrip.png"
    - "assets/objects/tamagushi.png"
```

## 必要な環境変数（例）

- `ARK_API_KEY`（公式ドキュメント準拠）
- `ARK_API_BASE`（デフォルト: `https://ark.ap-southeast.bytepluses.com/api/v3`）
- モデル:
  - `ARK_SEEDANCE_I2V_MODEL`（I2V）
  - `ARK_SEEDANCE_T2V_MODEL`（T2V）

互換のため、`ARK_API_KEY` が未設定なら `SEADREAM_API_KEY` をフォールバックで使う。

## オプション

- 音声:
  - デフォルトは `generate_audio=false`
  - 有効化: `--ark-generate-audio`（または `ARK_EXTRA_JSON` で上書き）
- 上級者向け:
  - `--ark-extra-json` / `ARK_EXTRA_JSON` でリクエスト payload をマージして拡張パラメータを渡せる

## 実装メモ

- ローカル画像は `data:image/<fmt>;base64,...` にエンコードして送る（File API upload は使っていない）。
  - 画像サイズが大きいとリクエストが重くなるため注意。

