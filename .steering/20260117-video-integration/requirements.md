# Video Generation Integration Requirements (Task 10)

## 目的
シーン単位の台本から **動画素材生成・合成・検証** までの統合要件を定義する。

## 参照
- `docs/video-generation.md`
- `workflow/video-manifest-template.md`
- `.steering/20260117-scene-loop/design.md`

## スコープ
- scene → assets の入出力インターフェース
- 画像/動画/TTSのプレースホルダ実装方針
- `scripts/render-video.sh` との連携
- 品質ゲート（長さ/比率/音ズレ/字幕）
- 失敗時のフォールバック方針

## 前提
- 画像/動画/TTSの本番プロバイダは未決定（TBD）
- MVPはプレースホルダ/モックでOK
- 出力は `video_manifest.md` を中心に管理

## 要件

### 1) Scene → Assets インターフェース
- 入力: scene_id, narration_text, visual_prompt, duration, constraints
- 出力: 画像/動画/音声のパス（manifestに記録）

### 2) プレースホルダ
- 画像/動画/TTS は **ダミー出力**で通す
- 実装は差し替え可能な構造であること

### 3) 合成
- `scripts/render-video.sh` を使い `video.mp4` を生成
- クリップリスト/ナレーション/字幕の入力を準備できること

### 4) 品質ゲート
- duration_ok, aspect_ratio_ok, audio_sync_ok, subtitle_ok を確認
- fail時は `state.txt` に記録

### 5) フォールバック
- 素材欠損時は `placeholder` を使用 or 生成を再試行

## 受け入れ条件
- scene → assets の契約が明記されている
- render-video.sh 連携が前提化されている
- 品質ゲートとフォールバックが定義されている
