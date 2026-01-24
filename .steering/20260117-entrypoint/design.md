# CLI / Entrypoint Design (Task 12)

## 目的
Claude Code の slash command を起点に、
最小限の入力で全体フローを起動できるようにする。

## 参照
- `.steering/20260117-entrypoint/requirements.md`
- `docs/system-architecture.md`

## 起動フロー

```
/toc-run "topic"
  → create output/<topic>_<timestamp>/
  → init state.txt
  → load config/system.yaml
  → run graph (or dry-run)
```

## Slash command 仕様

- コマンド名: `/toc-run`
- 引数:
  - `topic`（必須）
  - `--dry-run`（任意）
  - `--config`（任意）

## Dry-run 仕様

- 外部生成（画像/動画/TTS）を実行しない
- research/story/script のみ作成
- `video.mp4` は生成しない

## 設定読み込み

- `config/system.yaml` を既定とする
- `--config` で別ファイルを読み込める
- コマンド引数は設定を上書きできる

## 出力規則

- `output/<topic>_<timestamp>/` を作成
- `state.txt` を初期化（1ブロック目を追記）

## 受け入れ条件

- /toc-run の仕様が明文化されている
- dry-run で実行可能な範囲が定義されている
