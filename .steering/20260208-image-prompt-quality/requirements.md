# Requirements: 画像生成プロンプト品質の底上げ（Nano Banana Pro / cross-model）

## 背景 / 問題

- `video_manifest.md` の `scenes[].image_generation.prompt` が自由文になりやすく、**scene間でスタイル/視点/人物の一貫性が崩れる**。
- `/toc-immersive-ride` では「ride action boat / hands / safety bar / track」などの不変条件が重要だが、sceneごとに抜けたり表現が揺れたりして品質が落ちやすい。
- 現状の生成スクリプト（`scripts/generate-assets-from-manifest.py`）は `assets.character_bible` / `assets.style_guide` を読まず、**共通要素が“コピペ運用”**になっている。

## ゴール

- 画像生成（特に Nano Banana Pro / Gemini Image）で、**高品質・一貫性・再現性**を上げる。
- 「全体 → 個別（scene）」の流れで、prompt を **構造化（見出し/順序固定）**し、下流が迷わない状態にする。
- Midjourney 専用構文（`--ar` 等）に依存せず、**cross-model**で通用する表現に寄せる（ただし MJ と NanoBanana の両方で通る一般表現は採用可）。
- アニメ調（anime/cartoon/illustration）への寄りを避け、**photorealistic / cinematic / practical effects** を安定させる。

## 非ゴール / 除外

- アニメ/イラスト調を狙うためのプロンプト最適化。
- Midjourney 限定パラメータ（`--stylize`, `--weird`, `--niji`, など）を前提にした設計。
- 生成 API のコスト最適化やモデル選定の再検討（本タスクの中心ではない）。

## 成功指標（MVP）

- 1回の run で生成された全scene画像が、以下を満たす確率が上がる:
  - POV がぶれない（hands + safety bar が常に画面内）
  - キャラクターが“別人化”しにくい（参照画像 + 固定フレーズが効く）
  - scene間の連続性（照明/進行方向/位置関係）が破綻しにくい
- prompt が「どこに何を書くか」迷わず埋められる（テンプレ + 具体例がある）

