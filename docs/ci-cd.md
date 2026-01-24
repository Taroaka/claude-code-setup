# CI/CD & Deployment (MVP)

本書は `todo.txt` の 5) CI/CD & deployment pipeline を具体化する。

## 1. Container registry & tagging

- **Registry**: GitHub Container Registry (GHCR)
- **Tags**:
  - `latest` (main)
  - `sha-<short>` (commit)
  - `vX.Y.Z` (release tag)

## 2. Build/Test pipeline

- **CI**: GitHub Actions
- **最小チェック**:
  - Python 3.11 セットアップ
  - 依存インストール（`requirements.txt` がある場合）
  - `python -m compileall .`
  - Dry-run: `python scripts/build-clip-lists.py --help`
  - テストは存在する場合のみ実行（`tests/` があるとき）

## 3. Deploy workflow & rollback

- **デプロイ**: 当面は未実装（ローカル運用のみ）
- 将来:
  - `main` へのマージ → イメージビルド & push
  - ステージング/本番は手動承認
- **ロールバック**:
  - 直前の `sha-<short>` または `vX.Y.Z` タグへ切り戻し

## 4. Infra-as-code

- **MVP**: なし（Docker + docker-compose に限定）
- 将来: Terraform / Pulumi を検討

## 5. Observability

- **ログ**: stdout にJSONログ（将来）
- **メトリクス**: job実行時間/成功率/コストはDBに記録（設計のみ）
- **トレース**: 必要なら OpenTelemetry を追加

## 6. Health checks & timeouts

- **Health check**:
  - 将来のAPIサーバーは `/healthz` を用意
  - ワーカーはDB接続確認を最低条件にする
- **Timeouts**:
  - ステージ単位のタイムアウト
  - 失敗時はLangGraphでリトライ/中断を制御
