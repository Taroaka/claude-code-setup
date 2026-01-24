# Video Generation Integration Tasklist (Task 10)

## 仕様整理（Spec）

### 入出力
- **入力**: `script.md` + `video_manifest.md`
- **出力**: `video.mp4` + `assets/*` + `clips.txt` + `narration_list.txt`
- **状態**: `state.txt` に品質ゲート結果を追記

### 最小アセット構成
- 画像: `assets/scenes/scene{n}_base.png`
- 動画: `assets/scenes/scene{n}_video.mp4`
- 音声: `assets/audio/scene{n}_narration.mp3`

### 品質ゲート
- `duration_ok`, `aspect_ratio_ok`, `audio_sync_ok`, `subtitle_ok`

---

## 実装タスク

### 1) Manifest駆動の素材管理
- [ ] `video_manifest.md` に scene単位の素材パスを記録
- [ ] シーン番号とファイル命名の規則を固定
- [ ] 欠損素材の検出処理を追加

### 2) プレースホルダ生成
- [ ] 画像プレースホルダの生成（最小png）
- [ ] 動画プレースホルダの生成（静止画ループmp4）
- [ ] TTSプレースホルダ（無音 or テキストファイル）

### 3) クリップリストの生成
- [ ] `scripts/build-clip-lists.py` を呼び出す
- [ ] `*_clips.txt` と `*_narration_list.txt` を出力

### 4) レンダリング
- [ ] `scripts/render-video.sh` へ入力を渡し `video.mp4` を生成
- [ ] 任意で BGM / SRT を受け取れる構造にする

### 5) 品質ゲート
- [ ] 生成後に `duration_ok` を判定
- [ ] `aspect_ratio_ok` を判定
- [ ] `audio_sync_ok` / `subtitle_ok` を判定
- [ ] 結果を `state.txt` と manifest に記録

### 6) フォールバック
- [ ] 素材欠損時は placeholder を挿入
- [ ] 連続失敗は人間レビューへ

---

## 完了条件

- manifest 主導で素材が管理される
- mp4 が生成でき、品質ゲートが記録される
- 欠損素材があってもフォールバックで完走できる
