# Orchestration Artifacts & Logging Tasklist (Task 11)

## 仕様整理（Spec）

### 出力構成
- `orchestration_manifest.md`
- `run_report.md`
- `logs/` 配下に `*_input.json` / `*_output.json`

### ログ最小項目
- `job_id`, `stage`
- `input`, `output`
- `started_at`, `completed_at`, `duration_seconds`

---

## 実装タスク

### 1) マニフェスト生成
- [ ] `orchestration_manifest.md` の雛形を作成
- [ ] job/artifacts/gates/audit を記録
- [ ] state.txt と同期する項目を決める

### 2) ノード入出力ログ
- [ ] ステージごとの input/output を JSON 保存
- [ ] ファイル命名規則を固定（例: `STORY_input.json`）
- [ ] 文字コード/時刻フォーマットを統一

### 3) レビュー・QA記録
- [ ] Reviewer判定を audit に追記
- [ ] QAスコアを manifest に集約
- [ ] 重大指摘を run_report に反映

### 4) ランレポート
- [ ] jobサマリ（時間・コスト・品質）を記録
- [ ] 警告・失敗一覧を記載

### 5) 保存規則
- [ ] `output/<topic>_<timestamp>/` 配下に集約
- [ ] 失敗時も成果物を残す（再現性のため）

---

## 完了条件

- マニフェスト/ログ/レポートの出力が再現可能
- 各ステージのinput/outputが追跡できる
