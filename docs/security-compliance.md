# Security / Compliance / Legal (MVP)

本書は `todo.txt` の 3) Security / compliance / legal を具体化する。

## 1. Secrets management（環境変数管理）

- 秘密情報は **環境変数** で管理する。
- ローカル開発は `.env` を利用し、テンプレは `.env.example` に保存する。
- 秘密情報はリポジトリやDBに保存しない。
- 本番/デプロイ時は環境注入（CI/CD, secrets manager 等）に移行可能とする。

## 2. Access control（アクセス制御）

- MVPは **単一ユーザー前提** とする。
- 認証/認可の実装は行わない（将来の拡張で追加）。

## 3. Content policy & compliance（要決定）

- 著作権・肖像権・AI生成表記などのルールは、
  `docs/orchestration-and-ops.md` の `compliance_rules` を採用する。

## 4. Audit log requirements（要決定）

- 監査ログは **DBのみ** に保存する。
- 記録対象は以下を最小セットとする：
  - job_id, stage, reviewer, decision, notes, timestamp

## 5. License handling（要決定）

- 音楽 / SFX / フォントなどの素材は **生成AIで内製** する前提。
- 外部素材の利用は原則行わないため、ライセンスリスクは最小。
- 収集・記録する情報は **テキストベース**（プロンプト、モデル名、出力パス、生成日時）。
- 例外的に外部素材を使う場合は、出典/ライセンス/利用条件を必ず記録する。
