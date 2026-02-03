# Design: Veo シームレス改善

## 方針（best-effort）

### 1) 単体clip内のフェード/カット抑制

- `GenerateVideosConfig.negative_prompt` を利用して、フェード/カット/字幕/モンタージュ系を禁止方向に誘導する
- 併せて video prompt 側にも「single continuous take / no cuts」等を明示する

### 2) clip結合時の継ぎ目改善（chaining）

- 前の clip の **終盤フレーム**（`N` 秒前）を `ffmpeg` で抽出し、次 clip の first frame として入力する
- これにより、concat の「次clipの1フレ目が別物」になりにくくする

## 実装箇所

- `scripts/generate-assets-from-manifest.py`
  - `--video-negative-prompt` を追加
  - `--chain-first-frame-from-prev-video` と `--chain-first-frame-seconds-from-end` を追加
- `scripts/toc-immersive-ride-e2e.py` / `scripts/toc-immersive-ride-generate.sh`
  - 没入型ワークフローのデフォルトとして chaining と negative prompt を適用する

