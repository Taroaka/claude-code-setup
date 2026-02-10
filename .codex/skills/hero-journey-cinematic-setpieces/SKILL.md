---
name: hero-journey-cinematic-setpieces
description: |
  Hero’s Journey を保ちつつ、物語の主役級アイテム/舞台装置（setpiece/artifact）を “bible化” して映画品質へ引き上げる。
metadata:
  tags: story, hero-journey, cinematic, setpiece, props, immersive
---

## When to use

- 物語は成立しているが、映像化したときの“見せ場”が薄いとき
- 竜宮城/玉手箱のような「背景ではなく重要要素」を、キャラ同様に設計して一貫させたいとき
- 文字無し（字幕/看板/刻印なし）で、映像だけで理解が進む構成にしたいとき

## What to produce

- `video_manifest.md` の `assets.object_bible`（設計の正本）
- reference scene（`assets/objects/...png` を生成する scene）
- 各sceneの `image_generation.object_ids`（混ざり防止）

## Checklist（decision complete）

1) 主役級 object を抽出（英雄の旅フェーズに割当）
2) 各 object に以下を埋める:
   - `cinematic.role`（映画での役割）
   - `cinematic.visual_takeaways[]`（映像から与える情報）
   - `cinematic.spectacle_details[]`（メイン筋と無関係でも魅力的な要素）
   - `fixed_prompts[]`（材質/構造/機構/禁止を短文で）
3) `reference_images[]` を必ず用意し、対応する reference scene を manifest に追加
4) story scene では `object_ids: []|[...]` を必ず明示
5) prompt 見出しは `GLOBAL/CHARACTERS/PROPS/SCENE/CONTINUITY/AVOID` の順（正本参照）

## Where to look (source of truth)

- 設計/契約: `docs/implementation/asset-bibles.md`
- prompt の型: `docs/implementation/image-prompting.md`
- 実装（注入/ゲート）: `scripts/generate-assets-from-manifest.py`
- 運用（スキル編）: `workflow/playbooks/script/hero-journey-cinematic-setpieces.md`

