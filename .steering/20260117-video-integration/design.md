# Video Generation Integration Design (Task 10)

## 目的
`script.md` から素材生成 → 合成 → 検証までを **一貫した流れ**として定義する。

## 参照
- `docs/video-generation.md`
- `workflow/video-manifest-template.md`
- `scripts/render-video.sh`

## 全体フロー

```
script.md → video_manifest.md → assets生成 → clips/narration list → render-video.sh → video.mp4 → QA
```

## Scene → Assets インターフェース

### 入力（scene単位）
- `scene_id`
- `narration_text`
- `visual_prompt`
- `duration_seconds`
- `constraints`（aspect_ratio, language, resolution）

### 出力（scene単位）
- `assets/scenes/scene{n}_base.png`
- `assets/scenes/scene{n}_video.mp4`
- `assets/audio/scene{n}_narration.mp3`

### 記録先
- `video_manifest.md` の `scenes[]` に記録

## プレースホルダ実装（MVP）

- **画像**: 1pxの単色画像 or 既存テンプレを配置
- **動画**: 静止画ループの短尺mp4
- **TTS**: 無音ファイル or テキストを書き出したplaceholder
- 後からプロバイダ差し替え可能な構造にする

## 合成

### クリップリスト生成
- `scripts/build-clip-lists.py` を使って
  `*_clips.txt` / `*_narration_list.txt` を生成

### レンダリング
- `scripts/render-video.sh` により `video.mp4` を生成
- 入力:
  - clip list
  - narration
  - bgm（任意）
  - srt（任意）

## 品質ゲート

最低限以下をチェック:
- `duration_ok`
- `aspect_ratio_ok`
- `audio_sync_ok`
- `subtitle_ok`

結果は `state.txt` と `video_manifest.md` に記録。

## フォールバック戦略

- 画像/動画が欠損 → placeholderを使用
- TTSが欠損 → 無音で進行し、QAで警告
- 連続失敗時は人間レビューに昇格

## 受け入れ条件

- manifestを中心に素材が管理されている
- render-video.sh で mp4 を生成できる
- フォールバックが定義されている
