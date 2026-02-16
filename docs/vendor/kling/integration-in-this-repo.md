# Kling 連携（このリポジトリの実装）

このドキュメントは「このrepoで Kling をどう叩いているか」を、ソースコードに沿ってまとめたものです（公式/第三者ドキュメントの差分に耐えるための“実装正”）。

## どこが Kling を呼ぶ？

- Provider 実装: `toc/providers/kling.py`
- 生成フロー: `scripts/generate-assets-from-manifest.py`
- 単体 CLI（疎通用）: `scripts/generate-kling-video.py`

## manifest の tool 名

- `kling_3_0`: Kling 3.0（デフォルト）
- `kling_3_0_omni`: Kling 3.0 Omni（モデル名と extra JSON を切替）
- `google_veo_3_1`: Veo（代替）

## env（最低限）

- 公式（推奨）:
  - `KLING_ACCESS_KEY`: AccessKey
  - `KLING_SECRET_KEY`: SecretKey（JWT 署名に使用。コミット禁止）
- ゲートウェイ互換（任意）:
  - `KLING_API_KEY`: Bearer で送るキー（実装はヘッダ名/プレフィクスを変更可能）
- `KLING_API_BASE`: ベースURL（例: `https://api.klingai.com`）
- `KLING_VIDEO_MODEL`: 通常 Kling のモデル名（例: `kling-3.0`）
- `KLING_OMNI_VIDEO_MODEL`: Omni のモデル名（初期値は `kling-3.0-omni` だが、必要なら差し替え）

## env（エンドポイント差し替え）

ベンダ/ゲートウェイによってパスが異なる場合に備えて、以下は上書き可能です。

- `KLING_VIDEO_SUBMIT_PATH`（default: `/v1/videos/generations`）
- `KLING_VIDEO_STATUS_PATH_TEMPLATE`（default: `/v1/videos/generations/{operation_id}`）

## env（レスポンス抽出の差し替え）

submit/status の JSON 形が違う場合はパス候補を調整できます。

- `KLING_OPERATION_ID_PATHS`
- `KLING_STATUS_PATHS`
- `KLING_DONE_STATUSES`
- `KLING_FAILED_STATUSES`
- `KLING_VIDEO_URL_PATHS`

## env（認証ヘッダ差し替え）

デフォルトは `Authorization: Bearer <key>` 相当です。

- `KLING_API_KEY_HEADER`（default: `authorization`）
- `KLING_API_KEY_PREFIX`（default: `Bearer `）

## extra JSON の使いどころ（Omni含む）

`scripts/generate-assets-from-manifest.py` は、Kling の request payload に任意の JSON を deep-merge します。

- 通常: `KLING_EXTRA_JSON` または `--kling-extra-json`
- Omni: `KLING_OMNI_EXTRA_JSON` / `--kling-omni-extra-json`
  - `KLING_OMNI_EXTRA_JSON` が空なら、`KLING_EXTRA_JSON` をフォールバックします

「公式/第三者 docs のパラメータがこのrepoの固定フィールドに無い」場合は、まずここで通してから必要になった段階で正規フィールド化する方針です。
