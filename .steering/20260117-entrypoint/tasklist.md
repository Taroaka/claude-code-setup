# CLI / Entrypoint Tasklist (Task 12)

## 仕様整理（Spec）

### コマンド
- `/toc-run "topic"`
- オプション: `--dry-run`, `--config`

### 出力
- `output/<topic>_<timestamp>/`
- `state.txt` 初期化

### 依存
- `config/system.yaml`

---

## 実装タスク

### 1) Slash command
- [ ] `/toc-run` の定義（Claude Code）
- [ ] 引数のパースとバリデーション

### 2) 出力フォルダ初期化
- [ ] `output/<topic>_<timestamp>/` を作成
- [ ] `state.txt` を初期ブロックで作成

### 3) 設定読み込み
- [ ] `config/system.yaml` を読み込む
- [ ] `--config` の上書き対応

### 4) Dry-run 実装
- [ ] 外部生成をスキップするフラグ
- [ ] research/story/script のみ生成

---

## 完了条件

- /toc-run でパイプラインが起動できる
- dry-run が正常に動作する
