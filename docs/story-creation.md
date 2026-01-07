# Story Creation System

物語生成システム - Deep Researchの成果を1分動画向けの物語に加工する手順書

## 概要

このドキュメントは、`docs/information-gathering.md` で収集した構造化情報を、TikTok向け1分動画の物語に変換するための手順を定義する。

### 位置づけ

```
[情報収集] → [物語生成] → [動画生成]
              ↑ 本書
```

### 入力

- `output/research/{topic}_{timestamp}.md` - Deep Researchの出力ファイル
- 構造化YAML形式の知識ベース

### 出力

- `output/stories/{topic}_{timestamp}.md` - 物語スクリプト
- 1分（60秒）の動画用台本

---

## 物語構造：ヒーローズジャーニー

### 理論的背景

ヒーローズジャーニー（英雄の旅）は、1949年にジョセフ・キャンベルが『千の顔を持つ英雄』で体系化した普遍的物語構造。ジョージ・ルーカスがスターウォーズ制作に活用し、現代エンターテインメントの基礎となった。

**核心原理**: 人間は「変容」の物語に本能的に惹かれる。

### 1分動画への圧縮

17段階 → 12段階 → 8段階 → **3要素**に圧縮

```
┌─────────────────────────────────────────────────────────┐
│  [日常世界]  →  [試練/変容]  →  [新しい自分での帰還]  │
│   (0-5秒)       (5-50秒)         (50-60秒)             │
└─────────────────────────────────────────────────────────┘
```

| フェーズ | 時間 | 目的 | 必須要素 |
|---------|------|------|----------|
| **日常世界** | 0-5秒 | フック、共感 | 視聴者が「自分ごと」と感じる状況 |
| **試練/変容** | 5-50秒 | 緊張、発見 | 問題→格闘→洞察 の流れ |
| **帰還** | 50-60秒 | 満足、余韻 | 変容後の姿、学びの提示 |

### Dan Harmon ストーリーサークル（8段階）

より詳細な構造が必要な場合：

```
        1. 快適圏にいる
              ↓
    8. 変化している ← 2. 何かを望む
              ↑           ↓
    7. 帰還する      3. 未知に入る
              ↑           ↓
    6. 代償を払う → 4. 適応する
              ↑           ↓
              └── 5. 望みを得る
```

---

## 物語生成プロセス

### Phase 1: 素材分析（Research解析）

Deep Research出力から物語素材を抽出する。

#### Step 1.1: 主人公の特定

```yaml
protagonist_candidates:
  - source: knowledge_graph.nodes (type: Person)
  - criteria:
      - 変容を経験した人物
      - 困難を乗り越えた人物
      - 視聴者が共感できる人物
```

#### Step 1.2: エンゲージメントフックの選定

```yaml
hook_selection:
  source: engagement.hooks
  priority:
    1. hidden_truth (隠された真実)
    2. counterintuitive (常識の逆)
    3. mystery (未解決の謎)
    4. emotional (感情的共鳴)
    5. controversy (論争)
```

#### Step 1.3: テンションポイントの抽出

```yaml
tension_source: engagement.tension_points
usage:
  - 対立する視点を物語の葛藤に変換
  - 「でも実は...」の転換点として使用
```

### Phase 2: 物語設計

#### Step 2.1: SCQA構造の活用

Deep Researchの `synthesis.scqa` を物語骨格に変換：

| SCQA要素 | 物語での役割 | 動画での位置 |
|----------|-------------|-------------|
| Situation | 日常世界の設定 | 0-3秒 |
| Complication | 問題・葛藤の提示 | 3-10秒 |
| Question | 視聴者の疑問喚起 | 10-15秒（暗示） |
| Answer | 解決・洞察の提示 | 40-60秒 |

#### Step 2.2: So What チェーン適用

`synthesis.so_what_chain` を活用して、単なる事実を「意味のある洞察」に変換：

```
事実 → So What? → So What? → So What? → 最終洞察
                                          ↓
                                      物語のテーマ
```

#### Step 2.3: 感情曲線の設計

```
感情
 ↑
 │         ★ クライマックス
 │        / \
 │       /   \
 │      /     ★ 解決
 │ ★   /
 │  \ /
 │   ★ 葛藤深化
 │
 └──────────────────────→ 時間
   0s   15s   30s   45s   60s
```

### Phase 3: 脚本執筆

#### Step 3.1: オープニング（0-5秒）

**目的**: 視聴者を3秒以内に引き込む

**テクニック**:
- **疑問形**: 「なぜ〇〇は△△なのか？」
- **常識の否定**: 「〇〇は間違っている」
- **驚きの事実**: 「実は〇〇は△△だった」
- **感情的フック**: 「誰もが知っているあの物語の、誰も知らない真実」

**テンプレート**:
```
[視覚] 印象的な1カット
[音声] フック文（15-20文字以内）
[テキスト] 補助テロップ
```

#### Step 3.2: 本体（5-50秒）

**構造**:
```
[問題提示] 5-15秒
   ↓ 「でも...」「しかし...」
[葛藤深化] 15-30秒
   ↓ 「そして...」「ついに...」
[転換点] 30-40秒
   ↓ 「実は...」「だから...」
[解決への道] 40-50秒
```

**視覚変化ルール**:
- 1-3秒ごとにカット変更
- 静止画の場合はズーム/パンで動きを追加
- テキストは8文字以内/行

#### Step 3.3: エンディング（50-60秒）

**目的**: 満足感と余韻、ループ促進

**テクニック**:
- **変容の可視化**: Before → After を明示
- **学びの提示**: 「だから〇〇なのだ」
- **オープンループ**: 次回への伏線（シリーズの場合）
- **ループ構造**: 最初のシーンに戻る → 再生率200%

### Phase 4: 品質検証

#### Step 4.1: ヒーローズジャーニー適合チェック

```yaml
checklist:
  ordinary_world:
    present: true/false
    seconds: 0-5
  call_to_adventure:
    present: true/false
    type: question/problem/opportunity
  ordeal:
    present: true/false  # 必須
    tension_level: 1-10
  transformation:
    present: true/false  # 必須
    before_after_clear: true/false
  return:
    present: true/false
    satisfaction_level: 1-10
```

#### Step 4.2: エンゲージメント品質チェック

```yaml
engagement_checklist:
  hook_in_3_seconds: true/false  # 必須
  curiosity_maintained: true/false
  visual_change_frequency: "1-3秒" / "3-5秒" / "5秒以上"
  emotional_payoff: true/false
  loop_potential: true/false
```

#### Step 4.3: 情報正確性チェック

```yaml
accuracy_checklist:
  facts_from_research: true/false
  source_confidence: 0.0-1.0
  claims_verified: true/false
  no_fabrication: true/false
```

---

## 物語パターンライブラリ

### パターン1: 隠された真実型

```
[フック] 「誰もが知っている〇〇の、誰も知らない真実」
[展開] 常識の提示 → 「でも実は...」 → 隠された事実
[結末] 新しい理解、世界観の更新
```

**適用**: `engagement.hooks.type == "hidden_truth"` の場合

### パターン2: 逆説型

```
[フック] 「〇〇は△△だと思っていませんか？実は逆です」
[展開] 常識の否定 → 証拠の提示 → 真の理由
[結末] パラダイムシフト
```

**適用**: `engagement.hooks.type == "counterintuitive"` の場合

### パターン3: 謎解き型

```
[フック] 「なぜ〇〇は△△なのか？」
[展開] 謎の提示 → 手がかり1 → 手がかり2 → 解明
[結末] 「だから〇〇なのだ」
```

**適用**: `engagement.hooks.type == "mystery"` の場合

### パターン4: 英雄譚型

```
[フック] 「この人物が世界を変えた」
[展開] 困難な状況 → 決断 → 試練 → 勝利
[結末] 変容した姿、レガシー
```

**適用**: `knowledge_graph.nodes` に著名人物がいる場合

### パターン5: 感情共鳴型

```
[フック] 感情的な場面/言葉
[展開] 背景説明 → 感情の深化 → カタルシス
[結末] 普遍的な教訓
```

**適用**: `engagement.hooks.type == "emotional"` の場合

---

## 出力スキーマ

### 物語出力フォーマット

```yaml
# === メタ情報 ===
story_metadata:
  topic: "string"
  source_research: "output/research/{file}.md"
  created_at: "ISO8601"
  duration_seconds: 60
  pattern_used: "hidden_truth | counterintuitive | mystery | hero | emotional"

# === 物語構造 ===
story_structure:
  protagonist:
    name: "string"
    role: "string"
    source_node_id: "research内のnode id"

  journey:
    ordinary_world:
      description: "string"
      duration_seconds: 5

    call_to_adventure:
      trigger: "string"
      question_raised: "string"

    ordeal:
      challenge: "string"
      tension_elements:
        - "string"
      duration_seconds: 30

    transformation:
      before: "string"
      after: "string"
      insight: "string"

    return:
      resolution: "string"
      duration_seconds: 10

  theme:
    governing_thought: "string"
    universal_truth: "string"

# === 脚本 ===
script:
  total_duration: 60

  scenes:
    - scene_id: 1
      timestamp: "00:00-00:05"
      phase: "opening"

      visual:
        description: "string"
        type: "image | video | text_overlay"
        motion: "zoom_in | zoom_out | pan_left | pan_right | static"

      audio:
        narration: "string"
        narration_word_count: 20  # 目安: 3-4文字/秒
        bgm: "string"
        sfx: "string"

      text_overlay:
        main: "string"  # 8文字以内
        sub: "string"

      hook_type: "question | statement | shock | emotion"

    - scene_id: 2
      timestamp: "00:05-00:15"
      phase: "development"
      # ... 以下同様

    - scene_id: 3
      timestamp: "00:15-00:35"
      phase: "ordeal"

    - scene_id: 4
      timestamp: "00:35-00:50"
      phase: "transformation"

    - scene_id: 5
      timestamp: "00:50-01:00"
      phase: "ending"
      loop_point: true  # ループ再生を促す場合

# === エンゲージメント設計 ===
engagement_design:
  primary_hook:
    type: "string"
    content: "string"
    source: "engagement.hooks[n]"
    placement: "00:00-00:03"

  tension_arc:
    - timestamp: "00:10"
      tension_level: 3
      element: "問題提示"
    - timestamp: "00:25"
      tension_level: 7
      element: "葛藤深化"
    - timestamp: "00:40"
      tension_level: 9
      element: "クライマックス"
    - timestamp: "00:55"
      tension_level: 5
      element: "解決"

  retention_techniques:
    - technique: "open_loop"
      placement: "00:08"
      description: "疑問を提示して答えを後回し"
    - technique: "pattern_interrupt"
      placement: "00:20"
      description: "予想を裏切る展開"
    - technique: "loop_structure"
      placement: "00:55-01:00"
      description: "最初のシーンに視覚的に戻る"

# === 品質スコア ===
quality_scores:
  hero_journey_compliance: 0.0-1.0
  engagement_potential: 0.0-1.0
  information_accuracy: 0.0-1.0
  emotional_impact: 0.0-1.0

  checklist:
    hook_in_3_seconds: true
    ordeal_present: true
    transformation_clear: true
    facts_verified: true
    loop_ready: true

# === ソース追跡 ===
sources:
  facts_used:
    - fact: "string"
      source: "research.facts.xxx"
      confidence: 0.0-1.0

  hooks_used:
    - hook: "string"
      source: "research.engagement.hooks[n]"

  claims:
    - claim: "string"
      verification: "verified | unverified | partially_verified"
      source: "string"
```

---

## 代替フレームワーク

### ヒロインズジャーニー（女性主人公向け）

ヒーローズジャーニーが「上昇」構造なのに対し、ヒロインズジャーニーは「下降→再生→上昇」構造。

```
1. 男性的世界での成功への憧れ
2. 男性的成功の達成
3. 空虚さの認識
4. 下降（暗闘への旅）
5. 死（古い自己の死）
6. 女性的なものとの再接続
7. 男性的・女性的の統合
8. 帰還
```

**適用**: 女性主人公、内面の成長、自己発見がテーマの場合

### Save the Cat（15ビート）

より細かい構成管理が必要な場合：

| ビート | 位置 | 60秒換算 |
|--------|------|----------|
| Opening Image | 1% | 0-1秒 |
| Theme Stated | 5% | 3秒 |
| Set-Up | 1-10% | 1-6秒 |
| Catalyst | 10% | 6秒 |
| Debate | 10-25% | 6-15秒 |
| Break into Two | 25% | 15秒 |
| B Story | 30% | 18秒 |
| Fun and Games | 30-50% | 18-30秒 |
| Midpoint | 50% | 30秒 |
| Bad Guys Close In | 50-75% | 30-45秒 |
| All Is Lost | 75% | 45秒 |
| Dark Night of the Soul | 75-80% | 45-48秒 |
| Break into Three | 80% | 48秒 |
| Finale | 80-99% | 48-59秒 |
| Final Image | 99-100% | 59-60秒 |

---

## 制約と注意事項

### コンテンツガイドライン

```yaml
constraints:
  duration:
    target: 60
    min: 55
    max: 65

  narration:
    words_per_second: 3-4
    total_words: 180-240

  text_overlay:
    max_characters_per_line: 8
    max_lines: 2

  visual_change:
    max_static_duration: 3  # 秒

  accuracy:
    min_source_confidence: 0.7
    fabrication: prohibited
```

### 避けるべきパターン

1. **情報過多**: 1分に詰め込みすぎない（1つのテーマに集中）
2. **抽象的すぎる**: 具体的なエピソード、数字、人物を使う
3. **フックの弱さ**: 最初の3秒で視聴者を失う
4. **変容の不在**: 「だから何？」で終わらない
5. **事実の捏造**: Research出力にない情報を勝手に追加しない

---

## 実行フロー

```
1. Research出力の読み込み
   └→ output/research/{topic}_{timestamp}.md

2. 素材分析
   ├→ 主人公候補の抽出
   ├→ エンゲージメントフック選定
   └→ テンションポイント抽出

3. 物語パターン選択
   └→ フックタイプに基づく最適パターン

4. SCQA骨格構築
   └→ research.synthesis.scqa を変換

5. 脚本執筆
   ├→ オープニング（0-5秒）
   ├→ 本体（5-50秒）
   └→ エンディング（50-60秒）

6. 品質検証
   ├→ ヒーローズジャーニー適合
   ├→ エンゲージメント品質
   └→ 情報正確性

7. 出力
   └→ output/stories/{topic}_{timestamp}.md
```

---

## 参考文献

### 理論的基盤

- Campbell, Joseph. *The Hero with a Thousand Faces*. 1949.
- Vogler, Christopher. *The Writer's Journey: Mythic Structure for Writers*. 1992.
- Murdock, Maureen. *The Heroine's Journey*. 1990.
- Snyder, Blake. *Save the Cat!*. 2005.

### 短尺コンテンツ向け

- [Chris Vogler's Short Form Guide](https://chrisvogler.wordpress.com/2011/02/24/heros-journey-short-form/)
- [Dan Harmon's Story Circle](https://reedsy.com/blog/guide/story-structure/dan-harmon-story-circle/)

### 分析事例

- [The Script Lab - Star Wars Hero's Journey](https://thescriptlab.com/features/screenwriting-101/12309-the-heros-journey-breakdown-star-wars/)
- [神話の法則を千と千尋で解説](https://kkusaba.com/heros-journey/)
