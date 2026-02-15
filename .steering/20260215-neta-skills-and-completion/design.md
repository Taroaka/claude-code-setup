# Design: Neta collection skills + completion tracking + vertical shorts

## 1) Codex skills（ネタ収集）

### Placement / install

- 正本: `codex_skills/<skill-name>/SKILL.md`
- インストール: `scripts/ai/install-codex-skills.sh`（既存）

### Skills

- `neta-collector`（入口 / ルータ）
  - その1〜その4のどれをやるかを確認し、該当スキルの手順で出力する
- `selfhelp-trend-researcher`（その2）
  - “Hybrid”方針: Web検索できる環境なら候補と出典候補を列挙、できない環境なら未検証として TODO とリンク貼り付け依頼
  - 人物紹介（何者/主張/人気理由/批判点/出典）を主軸。金額・資産は Verified/Reported/Claimed/Unknown ラベルで扱う
- `ai-idea-studio`（その3）
  - 既存作品の固有要素を避けた “オリジナル案” を量産し、1案を ToCに落とす
- `era-explainer`（その4）
  - デフォルトは `cloud_island_walk`（概念をゾーンで散策して理解する）での解説
  - 未確定論点は “未検証” として検証観点を出す

## 2) state.txt（完成判断）

### Keys（追加）

- `runtime.stage=init|assets|render|done|shorts`（運用の目印）
- `runtime.render.status=started|success|failed`
- `artifact.video=output/<topic>_<timestamp>/video.mp4`
- `review.video.status=pending|approved|changes_requested`
- `review.video.note=string`
- `review.video.at=ISO8601`

### Helper script: `scripts/toc-state.py`

サブコマンド:

- `ensure --run-dir <dir> --manifest <manifest>`: state.txt が無ければ INIT を作る（topicはmanifestから読む）
- `append --run-dir <dir> --set key=value [--set ...]`: 最終状態を merge して snapshot を追記する（timestampは自動）
- `approve-video --run-dir <dir> [--note "..."]`: `review.video.status=approved` を追記
- `show --run-dir <dir>`: 最終状態の要点を表示

実装方針:
- 既存の “部分追記” state も壊さないため、読み込みは全ブロックを merge（後勝ち）して解釈する
- 追記は snapshot（既存状態+上書き+timestamp）として書く

### Wiring: `scripts/toc-immersive-ride-generate.sh`

- 冒頭で `toc-state.py ensure`
- 素材生成の前後、レンダリング開始/成功/失敗で `toc-state.py append` を呼ぶ
- 失敗時は trap で `runtime.render.status=failed` と `last_error` を追記する（可能な範囲）

## 3) Vertical shorts（中心cropで9:16）

### Script: `scripts/make-vertical-short.py`

- 入力: `--run-dir`, `--scene-ids 10,20,...`, `--out`, `--duration-seconds 60`
- Gate:
  - `review.video.status=approved` 以外は中断し、`toc-state.py approve-video` を案内
  - `artifact.video` または `<run_dir>/video.mp4` が存在すること
- 生成:
  - `video_manifest.md` の ```yaml から scene_id→timestamp を取り、該当区間を抽出して縦変換
  - cropフィルタは入力サイズ依存で中心crop（`crop=ih*9/16:ih:(iw-ih*9/16)/2:0`）
  - 60秒超過時は末尾をtrim
- 成功時に state へ追記:
  - `artifact.video.short.01=<path>`
  - `runtime.stage=shorts`

### Skill: `vertical-shorts-creator`

`make-vertical-short.py` を使う前提で、manifestから刺激強め scene を選ぶ手順と実行コマンドを出す。

