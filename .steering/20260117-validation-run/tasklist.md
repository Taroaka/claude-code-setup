# Validation Run Tasklist (Task 14)

## 仕様整理（Spec）

### 目的
- 既知トピックでE2E相当の確認を行い、成果物が揃うことを検証する

### 起動
- 起点: Claude Code の `/toc-run`
- 入力: `topic`（例: 桃太郎）
- モード: `--dry-run`（外部生成なしでも可）

### 期待成果物（最低限）
- `research.md`
- `story.md`
- `script.md`
- `video_manifest.md`
- `state.txt`
- `run_report.md`（Task11の記録方針に合わせる）
- `video.mp4` はプレースホルダでも可（Task10方針）

---

## 実行タスク

### 1) サンプル実行
- [ ] `/toc-run "桃太郎" --dry-run` を実行
- [ ] 出力フォルダ `output/桃太郎_<timestamp>/` が作成されること

### 2) 成果物確認
- [ ] `research.md` が存在する
- [ ] `story.md` が存在する
- [ ] `script.md` が存在する
- [ ] `video_manifest.md` が存在する
- [ ] `state.txt` が存在し、追記されている
- [ ] `run_report.md` が存在する（なければ生成方針を見直す）

### 3) ゲート/QA記録の確認
- [ ] QA結果が `run_report.md` または manifest に記録されている
- [ ] 重大エラーで停止していない

---

## 完了条件

- 指定トピックで成果物一式が揃う
- stateとQA記録が追跡可能
