# Script Method: Hero Journey × Cinematic Setpieces（スキル編）

## Use when

- “英雄の旅”の骨格はあるが、**映画としての見せ場（舞台装置/アイテム）が薄い**とき
- 竜宮城/玉手箱のように、背景ではなく「主役級 setpiece / artifact」を **映像だけで語りたい**とき
- 文字無し（字幕/看板/刻印なし）で、観客の理解と興味を前進させたいとき

## Goal

`video_manifest.md` を正本として、キャラ同様に:

1) `assets.object_bible` を設計（役割/映像情報/ショー性/固定ディテール）  
2) reference scene で参照画像を先に生成（`assets/objects/...png`）  
3) story scene では `object_ids` を宣言し、prompt に自動注入して一貫性を守る

## Output contract（最低限）

- `output/<topic>_<timestamp>/video_manifest.md`
  - `assets.object_bible[]`（reference_images / fixed_prompts は必須）
  - `scenes[].image_generation.object_ids: []|[...]`（必ず明示）

正本:
- `docs/implementation/asset-bibles.md`
- `docs/implementation/image-prompting.md`

---

## Workflow（decision complete）

### Step 1) “主役級 object” を抽出する（英雄の旅→見せ場）

英雄の旅フェーズごとに、最低1つは **物体/場所/現象**を割り当てる:

- 日常: “欠落/退屈” を見せる道具（対比のための地味さ）
- 境界（Threshold）: **門/橋/入口**（越境が映像でわかる setpiece）
- 試練/饗宴: “世界が広がる”ショー装置（観客の好奇心を稼ぐ）
- 誘惑/代償: **開けたくなる artifact**（禁忌の魅力が見た目で伝わる）
- 帰還/余韻: “変化の証拠”になる物（帰った後も残る違和感/学び）

### Step 2) object 1つずつ「設計」を埋める（映像情報まで）

各 object について、次の観点を埋める（埋まらないなら object 自体が弱い）:

1. **Role in film**（物語/感情/テーマでの役割）
2. **Visual takeaways**（観客が“映像だけで”理解する情報）
3. **Spectacle details**（メイン筋と無関係でもワクワクする見せ場/仕掛け）
4. **Physical reality**（材質/構造/重量感/工芸/経年）
5. **Mechanism / rules**（触れると反応、開封の不可逆、空間のルール）
6. **No-text constraint**（看板/刻印/字幕で説明しない）

→ 4〜6 を **短文の `fixed_prompts[]`** に落とす（下流がそのまま prompt に注入するため）。

### Step 3) reference scene を必ず作る（参照画像の先行生成）

- `assets.object_bible[].reference_images[]` の各パスを `scenes[].image_generation.output` として生成する scene を用意する
- reference scene の基本:
  - setpiece: 無人の外観/内観（人物を入れない、混ざり防止）
  - artifact: クローズアップ + 背景ニュートラル（材質/機構が読める）

### Step 4) story scene に `object_ids` を割り当てる（混ざり防止）

- 各 story scene の `image_generation.object_ids` に、その scene で映す object_id を列挙
- 何も無い scene でも `object_ids: []` を明示（ゲート用）

### Step 5) prompt へ注入する前提で構造化する

- prompt ブロック順（固定）:
  1. `GLOBAL / INVARIANTS`
  2. `CHARACTERS`
  3. `PROPS / SETPIECES`
  4. `SCENE`
  5. `CONTINUITY`
  6. `AVOID`
- “説明したい衝動” が出たら、文字ではなく **形/光/動き/ショー**に変換する。

---

## Example seed（浦島太郎）

- `ryugu_palace`（setpiece）:
  - Role: 境界 + 饗宴の誘惑（ここに居続けたくなる）
  - Visual takeaways: 城が生きている、海と建築が一体、時間が違う
  - Spectacle: 魚群のショー、泡のオーケストラ、潮流で動く光
- `tamatebako`（artifact）:
  - Role: 贈与 + 禁忌 + 代償（開けたくなる“間違い”）
  - Visual takeaways: ルールが箱に宿る、不可逆、近づくほど誘惑が増す
  - Spectacle: 呼吸する封印光、微細な振動、蓋の境界に溜まる灰粒

