# Data Lifecycle & Governance (MVP)

本書は `todo.txt` の 2) Data lifecycle & governance を具体化する。

## 1. Artifact taxonomy（成果物分類）

### Primary artifacts（成果物の本体）
- `research.md`：調査結果
- `story.md`：物語
- `script.md`：シーン台本（存在する場合）
- `video.mp4`：最終動画
- `video_manifest.md`：動画生成マニフェスト

### Derived artifacts（派生/中間）
- `assets/characters/*`：キャラクタ参照
- `assets/styles/*`：スタイル参照
- `assets/scenes/*`：シーン素材（静止画/動画）
- `assets/audio/*`：ナレーション/BGM/SFX
- `cache/llm/*.pkl`：設計段階のAI回答キャッシュ
- `clips.txt` / `narration_list.txt`：結合用リスト
- `improvement.md`：改善メモ

### Operational artifacts（運用）
- 生成ログ（DBまたはJSON）
- QA結果（スコア・判定）
- 実行メタデータ（job/run/step情報）

## 2. Retention policy（保持期間）

- **成功成果物は永久保存**（当面は削除しない）
  - primary/derived artifacts と manifest を対象
- **一時ファイルのみ自動削除対象**
  - `tmp/`, `*.tmp`, `*_draft.*` など

## 3. Data lineage（由来/系譜の追跡）

**目的**: source → prompt → asset → mp4 の流れを追跡可能にする。

### 追跡対象
- `job_id` / `run_id`
- ステージ（RESEARCH / STORY / SCRIPT / VIDEO / QA）
- 入力参照（上流成果物のパス/ID）
- プロンプト / 生成パラメータ
- プロバイダ名 / モデル名 / バージョン
- 出力パス
- ハッシュ（SHA-256 推奨）
- タイムスタンプ、所要時間、コスト概算

### 最小の系譜レコード（例）

```yaml
lineage_record:
  job_id: "JOB_20260113_0001"
  run_id: "RUN_0001"
  stage: "VIDEO"
  input_refs:
    - "output/<topic>_<timestamp>/story.md"
  provider:
    name: "google_veo_3_1"
    model: "veo-3.1-generate-preview"
    version: "preview"
  params:
    seed: 1234
    prompt: "string"
  output:
    path: "output/<topic>_<timestamp>/assets/scenes/scene1_video.mp4"
    sha256: "..."
  timing:
    started_at: "ISO8601"
    completed_at: "ISO8601"
    duration_seconds: 12.3
  cost:
    usd: 0.12
```

## 4. Naming / versioning scheme（命名）

- ルート: `output/<topic>_<timestamp>/`
- 再実行で衝突する場合は suffix を付ける：
  - `output/<topic>_<timestamp>_r02/`
- `run_id` はメタデータに必ず記録（ファイル名に埋め込む必要はない）

## 5. Caching policy（キャッシュ）

- **設計段階のAI回答のみキャッシュ**
  - 文字列/JSON出力は `pkl` で保存
  - 画像/動画は成果物として保存し、キャッシュ扱いはしない

## 6. Cleanup job（クリーンアップ）

**目的**: 永久保存ポリシーを維持しつつ、ゴミファイルを除去する。

- 対象:
  - `tmp/` 配下
  - `*.tmp`, `*_draft.*`
  - 途中生成で不要になった中間物（フラグ付き）
- タイミング:
  - ジョブ完了後に都度実行
  - もしくは日次のバッチ（手動/cron）
- 削除しない:
  - primary/derived artifacts
  - manifest, QA結果, 生成ログ
