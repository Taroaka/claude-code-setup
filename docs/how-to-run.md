# How to Run (MVP)

本書は `todo.txt` の 15) Documentation に対応する。

## 前提
- 起点は Claude Code の slash command（例: `/toc-run`）
- 成果物は `output/<topic>_<timestamp>/` に生成される
- state は `output/<topic>_<timestamp>/state.txt`（追記型）

## セットアップ（Docker）

1) `.env.example` を `.env` にコピーし、APIキー等を設定する  
2) 起動:

```bash
docker-compose up --build
```

## 実行（想定）

Claude Code で以下を実行:

```
/toc-run "桃太郎" --dry-run
```

## 期待される出力

```
output/<topic>_<timestamp>/
  state.txt
  research.md
  story.md
  script.md
  video_manifest.md
  video.mp4          (プレースホルダでも可)
  run_report.md
  logs/
```

## 生成（画像/動画/TTS）について

- 画像/動画/TTS の本番プロバイダは未決定（TBD）
- 当面はプレースホルダ生成（モック）でフローを検証する
- 具体は `.steering/20260117-video-integration/design.md` を参照

## state運用

- `state.txt` は追記型（最新ブロックが現在状態）
- 擬似ロールバックは「過去ブロックのコピーを末尾に追記」で再現する
- スキーマは `workflow/state-schema.txt` を参照
