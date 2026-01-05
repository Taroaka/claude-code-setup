# 情報収集手順書（Deep Research System）

## 概要

ユーザーが入力したトピックに対して、多角的・多層的に情報を収集し、構造化された知識ベースを生成するシステム。

```
[トピック入力] → [多層的情報収集] → [オントロジーマッピング] → [MECE検証] → [フック抽出] → [構造化知識ベース]
```

## 設計原則

### 教科書的網羅性（Comprehensive Coverage）

- **MECE原則**: Mutually Exclusive, Collectively Exhaustive（漏れなくダブりなく）
- **Bloom's Taxonomy**: 認知レベルの階層的整理
- **オントロジー**: エンティティと関係性の形式的定義

### エンゲージメント価値（Engagement Value）

- **Curiosity Gap**: 「知っていること」と「知りたいこと」のギャップ
- **Open Loop**: 未解決の問いによる興味維持
- **Tension Points**: 対立・論争による緊張感

## 情報収集の階層

### Level 1: 原典・一次資料

最優先で取得。全文テキストの確保を目指す。

| ソース | 対象 | API/取得方法 |
|--------|------|-------------|
| 青空文庫 | 著作権切れ日本文学 | API / GitHub Raw |
| 国立国会図書館デジタル | 古典・歴史資料 | NDL Search API |
| 古典籍総合データベース | 古典籍画像・翻刻 | NIJL API |
| Project Gutenberg | 著作権切れ英語文学 | API / Mirror |
| Internet Archive | 書籍・音声・映像 | API |

### Level 2: 学術・研究

学術的な裏付け・解釈を取得。

| ソース | 対象 | API/取得方法 |
|--------|------|-------------|
| CiNii Research | 日本の学術論文 | CiNii API |
| J-STAGE | 学術誌・紀要 | J-STAGE API |
| Google Scholar | 学術論文全般 | SerpAPI / スクレイピング |
| 大学リポジトリ | 学位論文・研究成果 | OAI-PMH |
| JSTOR | 海外学術誌 | JSTOR API |

### Level 3: 百科事典・解説

基礎情報・構造化データを取得。

| ソース | 対象 | API/取得方法 |
|--------|------|-------------|
| Wikipedia | 概要・解説（多言語） | MediaWiki API |
| Wikidata | 構造化データ・関連性 | SPARQL / API |
| コトバンク | 国語辞典・百科事典 | スクレイピング |
| ブリタニカ | 専門的解説 | API / スクレイピング |
| DBpedia | Wikipedia構造化版 | SPARQL |

### Level 4: 考察・解釈・民間知識

多様な視点・解釈を取得。

| ソース | 対象 | API/取得方法 |
|--------|------|-------------|
| Web検索 | ブログ・記事・考察 | Google/Bing API |
| Reddit | 海外の議論・考察 | Reddit API |
| Quora | Q&A形式の知識 | スクレイピング |
| YouTube | 解説動画トランスクリプト | YouTube Data API |
| note/Zenn | 日本語の考察記事 | スクレイピング |

## オントロジー定義

### エンティティタイプ

```yaml
entity_types:
  Person:
    properties:
      - name: string
      - aliases: [string]
      - era: string
      - role: string
      - description: string

  Place:
    properties:
      - name: string
      - coordinates: [lat, lon]
      - significance: string
      - current_status: string

  Event:
    properties:
      - name: string
      - date: string
      - description: string
      - participants: [Person]
      - location: Place

  Concept:
    properties:
      - name: string
      - definition: string
      - domain: string
      - related_concepts: [Concept]

  Work:
    properties:
      - title: string
      - type: string  # 小説/映画/漫画/歌など
      - creator: Person
      - created_date: string
      - description: string
```

### 関係性タイプ

```yaml
relationship_types:
  # 因果関係
  - caused_by: "AはBによって引き起こされた"
  - led_to: "AはBにつながった"

  # 影響関係
  - influenced_by: "AはBに影響を受けた"
  - inspired: "AはBに影響を与えた"

  # 空間関係
  - located_in: "AはBに位置する"
  - originated_from: "AはBを起源とする"

  # 時間関係
  - preceded_by: "AはBの前に起きた"
  - followed_by: "AはBの後に起きた"
  - contemporary_with: "AはBと同時代"

  # 派生関係
  - derived_from: "AはBから派生した"
  - variant_of: "AはBの変形である"

  # 所属関係
  - part_of: "AはBの一部である"
  - contains: "AはBを含む"

  # 対立関係
  - contrasts_with: "AはBと対照的である"
  - contradicts: "AはBと矛盾する"
```

## MECE検証フレームワーク

収集した知識が「漏れなくダブりなく」かを検証する。

### 検証次元

```yaml
mece_dimensions:
  temporal:           # 時間軸
    - past            # 起源・歴史
    - present         # 現在の状況・解釈
    - future          # 影響・展望

  perspective:        # 視点
    - protagonist     # 主体・主人公視点
    - antagonist      # 対立者・敵役視点
    - observer        # 第三者・傍観者視点
    - meta            # メタ・作者視点

  abstraction:        # 抽象度
    - concrete        # 具体的事実
    - interpretive    # 解釈・分析
    - meta            # メタ分析・批評

  source_type:        # 情報源タイプ
    - primary         # 一次資料
    - secondary       # 二次資料（学術）
    - tertiary        # 三次資料（百科事典）
    - informal        # 非公式（ブログ等）

  sentiment:          # 感情・評価
    - positive        # 肯定的
    - neutral         # 中立
    - negative        # 否定的・批判的
```

### 検証プロセス

```
1. 収集した情報を各次元でタグ付け
2. 次元ごとのカバレッジを算出
3. ギャップ（未収集の観点）を特定
4. 重複（同一内容の重複）を検出
5. ギャップに対して追加収集を実行
```

## エンゲージメントフック抽出

各情報から「興味を引くポイント」を抽出・タグ付けする。

### フックタイプ

```yaml
hook_types:
  mystery:            # 謎・未解明
    description: "未だ解明されていない謎"
    example: "なぜ桃から生まれたのか、諸説あり決着していない"
    curiosity_trigger: "答えを知りたい"

  counterintuitive:   # 直感に反する
    description: "常識や直感に反する事実"
    example: "鬼は実は被害者だった説がある"
    curiosity_trigger: "本当に？詳しく知りたい"

  hidden_truth:       # 隠された真実
    description: "あまり知られていない事実"
    example: "99%の人が知らない桃太郎の原典では..."
    curiosity_trigger: "自分は知らない側かも"

  emotional:          # 感情を揺さぶる
    description: "感動・恐怖・驚きなど感情に訴える"
    example: "桃太郎の本当の結末は悲劇だった"
    curiosity_trigger: "感情的に惹きつけられる"

  connection:         # 意外なつながり
    description: "予想外の関連性"
    example: "桃太郎と古代ペルシャ神話の共通点"
    curiosity_trigger: "そんなつながりが？"

  controversy:        # 論争・対立
    description: "専門家の間でも意見が分かれる"
    example: "桃太郎の起源は岡山か香川か、論争が続く"
    curiosity_trigger: "どちらが正しいのか"
```

### Curiosity Score算出

```
curiosity_score = (
    novelty_factor      * 0.3 +   # 新規性（知られていない度合い）
    emotional_impact    * 0.25 +  # 感情的インパクト
    controversy_level   * 0.2 +   # 議論の余地
    relatability        * 0.15 +  # 共感・関連性
    actionability       * 0.1     # 「誰かに話したい」度
)
```

## 認知レベルタグ（Bloom's Taxonomy）

情報を認知レベルで分類し、深さのバランスを確認する。

```yaml
cognitive_levels:
  remember:           # 記憶：事実の想起
    description: "基本的な事実・データ"
    examples:
      - "桃太郎は室町時代末期に成立"
      - "主要キャラクターは桃太郎、犬、猿、雉"

  understand:         # 理解：意味の把握
    description: "事実の背景・理由の理解"
    examples:
      - "桃が選ばれた理由は中国の桃信仰に由来"
      - "きびだんごは吉備国（岡山）との関連を示唆"

  apply:              # 応用：知識の適用
    description: "他の文脈への適用"
    examples:
      - "桃太郎の構造は他の英雄譚にも見られる"
      - "現代のコンテンツにおける桃太郎モチーフ"

  analyze:            # 分析：構造の解明
    description: "要素間の関係性分析"
    examples:
      - "桃太郎の物語構造はキャンベルの英雄の旅に従う"
      - "登場人物の象徴的意味の分析"

  evaluate:           # 評価：判断・批評
    description: "価値判断・批評"
    examples:
      - "柳田國男の解釈 vs 現代の再解釈の比較評価"
      - "芥川龍之介版の文学的価値"

  create:             # 創造：新たな生成
    description: "新しい視点・解釈の創出"
    examples:
      - "現代社会における桃太郎の新解釈"
      - "異なる文化圏との比較から見える新たな意味"
```

## 構造化スキーマ

### 完全版スキーマ

```yaml
# === 基本情報 ===
topic: string
aliases: [string]

# === 原典情報 ===
primary_source:
  full_text: string
  source: string
  source_url: string
  original_date: string
  author: string
  variants:                     # 異本・バリエーション
    - version_name: string
      differences: string
      source: string

# === 知識グラフ ===
knowledge_graph:
  nodes:
    - id: string
      type: Person|Place|Event|Concept|Work
      label: string
      properties: {}
  edges:
    - from: node_id
      to: node_id
      relation: string          # relationship_typesから選択
      description: string
      source: string

# === 事実情報 ===
facts:
  origin:
    description: string
    sources: [string]
    confidence: float
  timeline:
    - date: string
      event: string
      source: string
      cognitive_level: string   # Bloom's Taxonomy
  geography:
    - place: string
      relevance: string
      coordinates: [lat, lon]
  people:
    - name: string
      role: string
      description: string

# === 解釈・考察 ===
interpretations:
  academic:
    - claim: string
      author: string
      source: string
      year: int
      cognitive_level: string
  cultural:
    - aspect: string
      description: string
      source: string
  controversies:
    - topic: string
      positions: [string]
      sources: [string]
      resolution_status: string  # resolved|ongoing|unknown

# === 関連情報 ===
connections:
  related_works:
    - title: string
      type: string
      relation: string
  influences:
    - direction: gave|received
      target: string
      description: string
  cross_references:
    - topic: string
      relation: string

# === エンゲージメント価値 ===
engagement:
  hooks:
    - type: mystery|counterintuitive|hidden_truth|emotional|connection|controversy
      content: string
      target_emotion: string
      curiosity_score: float
  tension_points:
    - topic: string
      positions: [string]
      narrative_potential: string
  open_questions:
    - question: string
      known_theories: [string]
      investigation_status: string

# === MECE検証結果 ===
mece_coverage:
  dimensions:
    temporal:
      past: float       # 0.0-1.0
      present: float
      future: float
    perspective:
      protagonist: float
      antagonist: float
      observer: float
    abstraction:
      concrete: float
      interpretive: float
      meta: float
  gaps:                 # 未収集の観点
    - dimension: string
      value: string
      priority: high|medium|low
  overlaps:             # 重複情報
    - items: [string]
      action: merge|keep_both|discard

# === 認知レベル分布 ===
cognitive_distribution:
  remember: int         # 該当情報数
  understand: int
  apply: int
  analyze: int
  evaluate: int
  create: int

# === メタ情報 ===
metadata:
  collected_at: datetime
  sources_used: [string]
  confidence_score: float
  completeness_score: float  # MECE充足度
  engagement_score: float    # フック充実度
```

## 収集プロセス

### Step 1: トピック正規化

```
入力: "桃太郎"
    ↓
正規化処理:
  - 別名展開: ["桃太郎", "ももたろう", "Momotaro", "Momotarō"]
  - 関連キーワード: ["桃太郎伝説", "桃太郎神社", "鬼ヶ島"]
  - ドメイン推定: "日本昔話", "民話", "伝承"
  - オントロジータイプ推定: Work (物語作品)
```

### Step 2: 一次資料の取得

```
優先順位:
1. 青空文庫で全文検索 → 全文テキスト取得
2. 国会図書館で原典検索 → デジタル資料取得
3. 複数バージョンがある場合は全て取得
4. 異本・バリエーションを variants に記録
```

### Step 3: 多角的情報収集

各レベルから並列で情報取得。

```
[Level 1: 原典] ──┐
[Level 2: 学術] ──┼──→ [情報プール]
[Level 3: 百科] ──┤
[Level 4: 考察] ──┘
```

### Step 4: オントロジーマッピング

```
収集した情報から:
1. エンティティを抽出 → nodes に追加
2. 関係性を特定 → edges に追加
3. 知識グラフを構築
```

### Step 5: MECE検証

```
1. 各次元でカバレッジを算出
2. ギャップを特定 → gaps に記録
3. 重複を検出 → overlaps に記録
4. 優先度の高いギャップに対して追加収集
```

### Step 6: フック抽出

```
収集した情報から:
1. 謎・未解明点を抽出 → hooks (mystery)
2. 直感に反する事実を抽出 → hooks (counterintuitive)
3. 論争点を抽出 → tension_points
4. 未解決の問いを抽出 → open_questions
5. curiosity_score を算出
```

### Step 7: 認知レベル分類

```
各情報に対して:
1. Bloom's Taxonomy でレベルを判定
2. cognitive_level タグを付与
3. 分布を cognitive_distribution に集計
4. バランスが偏っていれば追加収集
```

### Step 8: 構造化・統合

```
[情報プール] → [スキーママッピング] → [構造化知識ベース]
                      ↓
              重複排除・正規化
                      ↓
              スコア算出:
              - confidence_score
              - completeness_score
              - engagement_score
```

## 品質基準

### 必須フィールド

以下は必ず取得を試みる：

- `topic` - トピック名
- `primary_source.full_text` または `primary_source.source` - 原典情報
- `facts.origin` - 起源・成立情報
- `knowledge_graph.nodes` - 最低3つのエンティティ
- `engagement.hooks` - 最低2つのフック
- `metadata.sources_used` - 使用ソース一覧

### 信頼度スコアリング

| スコア | 基準 |
|--------|------|
| 0.9-1.0 | 一次資料から直接取得 |
| 0.7-0.9 | 学術論文・公式情報源 |
| 0.5-0.7 | Wikipedia等の編集済み百科事典 |
| 0.3-0.5 | 個人ブログ・考察（複数一致） |
| 0.0-0.3 | 単一の非公式ソース |

### 完全性スコアリング（MECE）

| スコア | 基準 |
|--------|------|
| 0.9-1.0 | 全次元で80%以上カバー、ギャップなし |
| 0.7-0.9 | 主要次元でカバー、軽微なギャップあり |
| 0.5-0.7 | 一部次元に明確なギャップ |
| 0.3-0.5 | 複数次元でギャップ |
| 0.0-0.3 | 大部分が未収集 |

### エンゲージメントスコアリング

| スコア | 基準 |
|--------|------|
| 0.9-1.0 | 5種類以上のフック、高curiosity_score |
| 0.7-0.9 | 3-4種類のフック、tension_pointあり |
| 0.5-0.7 | 2種類のフック |
| 0.3-0.5 | 1種類のフックのみ |
| 0.0-0.3 | フックなし |

## エラーハンドリング

| 状況 | 対応 |
|------|------|
| 一次資料が見つからない | Level 2-3 から概要を構築、`primary_source` を欠損マーク |
| API レート制限 | 指数バックオフでリトライ、代替ソースへフォールバック |
| 矛盾する情報 | 両論併記、controversies に記録、信頼度の高いソースを優先表示 |
| トピックが曖昧 | 候補を列挙してユーザーに確認 |
| MECE ギャップ検出 | 優先度に応じて追加収集を実行 |
| フック不足 | Level 4（考察・民間知識）を重点的に追加収集 |

## 使用例

### 入力

```
トピック: 桃太郎
```

### 出力（抜粋）

```yaml
topic: "桃太郎"
aliases: ["ももたろう", "Momotaro"]

primary_source:
  full_text: "むかしむかし、あるところに、おじいさんとおばあさんが..."
  source: "青空文庫 - 楠山正雄『桃太郎』"
  source_url: "https://www.aozora.gr.jp/..."
  original_date: "室町時代末期（原型）"
  variants:
    - version_name: "御伽草子版"
      differences: "桃を食べて若返った老夫婦から生まれる"
      source: "国立国会図書館デジタル"

knowledge_graph:
  nodes:
    - id: momotaro
      type: Person
      label: "桃太郎"
      properties:
        role: "主人公"
        origin: "桃から誕生"
    - id: oni
      type: Person
      label: "鬼"
      properties:
        role: "敵役"
        location: "鬼ヶ島"
    - id: onigashima
      type: Place
      label: "鬼ヶ島"
      properties:
        model: "女木島（香川県）説あり"
  edges:
    - from: momotaro
      to: oni
      relation: "contrasts_with"
      description: "善vs悪の対立構造"
    - from: oni
      to: onigashima
      relation: "located_in"

facts:
  origin:
    description: "室町時代末期に成立したとされる日本の昔話"
    sources: ["国文学研究資料館", "Wikipedia"]
    confidence: 0.85
  geography:
    - place: "岡山県"
      relevance: "桃太郎伝説発祥の地の一つ"
    - place: "女木島（鬼ヶ島）"
      relevance: "鬼ヶ島のモデルとされる"

interpretations:
  academic:
    - claim: "桃太郎は大和朝廷の吉備国平定を反映している"
      author: "柳田國男"
      source: "『桃太郎の誕生』"
      year: 1933
      cognitive_level: "analyze"
  controversies:
    - topic: "桃太郎発祥地論争"
      positions: ["岡山県説", "香川県説", "愛知県説"]
      sources: ["各県観光協会", "民俗学研究"]
      resolution_status: "ongoing"

engagement:
  hooks:
    - type: mystery
      content: "なぜ『桃』から生まれたのか - 中国の桃信仰との関連"
      target_emotion: "知的好奇心"
      curiosity_score: 0.85
    - type: counterintuitive
      content: "芥川龍之介版では鬼が被害者として描かれる"
      target_emotion: "驚き"
      curiosity_score: 0.9
    - type: hidden_truth
      content: "原典（御伽草子版）では老夫婦が桃を食べて若返り、その後に生まれた"
      target_emotion: "発見"
      curiosity_score: 0.8
  tension_points:
    - topic: "桃太郎は正義か侵略者か"
      positions: ["伝統的解釈：鬼退治の英雄", "現代的再解釈：一方的な侵略者"]
      narrative_potential: "価値観の転換を促す議論ネタ"
  open_questions:
    - question: "きびだんごの『きび』は吉備国か黍か"
      known_theories: ["吉備国説", "穀物の黍説"]
      investigation_status: "諸説あり"

mece_coverage:
  dimensions:
    temporal:
      past: 0.9
      present: 0.7
      future: 0.3
    perspective:
      protagonist: 0.9
      antagonist: 0.6
      observer: 0.5
  gaps:
    - dimension: "temporal"
      value: "future"
      priority: "low"
    - dimension: "perspective"
      value: "antagonist"
      priority: "medium"

cognitive_distribution:
  remember: 12
  understand: 8
  apply: 4
  analyze: 6
  evaluate: 3
  create: 2

metadata:
  collected_at: "2026-01-05T12:00:00Z"
  sources_used:
    - "青空文庫"
    - "Wikipedia"
    - "CiNii"
    - "国立国会図書館"
  confidence_score: 0.82
  completeness_score: 0.75
  engagement_score: 0.85
```
