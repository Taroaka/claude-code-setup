# CLI / Entrypoint Requirements (Task 12)

## 目的
システムの起動方法と実行オプションを明確化し、
再現可能な実行フローを提供する。

## 参照
- `docs/system-architecture.md`
- `docs/data-contracts.md`

## スコープ
- Claude Code の slash command による起動
- dry-run の挙動
- 設定ファイル読み込み（YAML）
- 出力フォルダの決定規則

## 前提
- CLIサーバは作らない
- 起点は slash command

## 要件

### 起動
- Claude Code の slash command から起動できる
- 入力: topic（タイトル）

### 出力
- `output/<topic>_<timestamp>/` を作成する
- `state.txt` を初期化する

### dry-run
- 外部生成をスキップ
- `research.md` / `story.md` / `script.md` を生成

### 設定ファイル
- `config/system.yaml` を読み込む
- 実行時に上書きできる

## 受け入れ条件
- 起動条件/出力/設定読み込みが明記されている
