# 情報収集手順書（Deep Research System）

## 概要

ユーザーが入力したトピックに対して、多角的・多層的に情報を収集し、構造化された知識ベースを生成するシステム。

```
[トピック入力] → [多層的情報収集] → [構造化された知識ベース]
```

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

## 構造化スキーマ

収集した情報は以下のスキーマで統合する。

```yaml
topic: string                    # メイントピック
aliases:                         # 別名・表記ゆれ
  - string

primary_source:                  # 原典情報
  full_text: string              # 全文テキスト
  source: string                 # 出典元
  source_url: string             # 取得URL
  original_date: string          # 成立年代
  author: string                 # 著者（判明している場合）

facts:                           # 事実情報
  origin:                        # 起源・成立
    description: string
    sources: [string]
  timeline:                      # 時系列
    - date: string
      event: string
      source: string
  geography:                     # 関連地理
    - place: string
      relevance: string
      coordinates: [lat, lon]
  people:                        # 関連人物
    - name: string
      role: string
      description: string

interpretations:                 # 解釈・考察
  academic:                      # 学術的解釈
    - claim: string
      author: string
      source: string
      year: int
  cultural:                      # 文化的意味
    - aspect: string
      description: string
      source: string
  controversies:                 # 議論・異説
    - topic: string
      positions: [string]
      sources: [string]

connections:                     # 関連情報
  related_works:                 # 関連作品
    - title: string
      type: string               # 小説/映画/漫画など
      relation: string           # 原作/派生/パロディなど
  influences:                    # 影響関係
    - direction: string          # gave/received
      target: string
      description: string
  cross_references:              # 他トピック参照
    - topic: string
      relation: string

trivia:                          # 雑学・豆知識
  - fact: string
    source: string

metadata:                        # メタ情報
  collected_at: datetime
  sources_used: [string]
  confidence_score: float        # 情報の信頼度
```

## 収集プロセス

### Step 1: トピック正規化

```
入力: "桃太郎"
    ↓
正規化処理:
  - 別名展開: ["桃太郎", "ももたろう", "Momotaro", "Momotarō"]
  - 関連キーワード: ["桃太郎伝説", "桃太郎神社", "鬼ヶ島"]
  - カテゴリ推定: "日本昔話", "民話", "伝承"
```

### Step 2: 一次資料の取得

```
優先順位:
1. 青空文庫で全文検索 → 全文テキスト取得
2. 国会図書館で原典検索 → デジタル資料取得
3. 複数バージョンがある場合は全て取得
```

### Step 3: 多角的情報収集

各レベルから並列で情報取得。

```
[Level 1] ──┐
[Level 2] ──┼──→ [情報プール]
[Level 3] ──┤
[Level 4] ──┘
```

### Step 4: クロスリファレンス

```
収集した情報間の:
- 矛盾の検出 → フラグ付け
- 補完関係の特定 → マージ
- 信頼度の評価 → スコアリング
  - 一次資料: 高
  - 学術論文: 高
  - Wikipedia: 中
  - ブログ・考察: 低（複数一致で上昇）
```

### Step 5: 構造化・統合

```
[情報プール] → [スキーママッピング] → [構造化知識ベース]
                      ↓
              重複排除・正規化
                      ↓
              欠損フィールド特定
                      ↓
              追加収集 or 欠損マーク
```

## 品質基準

### 必須フィールド

以下は必ず取得を試みる：

- `topic` - トピック名
- `primary_source.full_text` または `primary_source.source` - 原典情報
- `facts.origin` - 起源・成立情報
- `metadata.sources_used` - 使用ソース一覧

### 信頼度スコアリング

| スコア | 基準 |
|--------|------|
| 0.9-1.0 | 一次資料から直接取得 |
| 0.7-0.9 | 学術論文・公式情報源 |
| 0.5-0.7 | Wikipedia等の編集済み百科事典 |
| 0.3-0.5 | 個人ブログ・考察（複数一致） |
| 0.0-0.3 | 単一の非公式ソース |

## エラーハンドリング

| 状況 | 対応 |
|------|------|
| 一次資料が見つからない | Level 2-3 から概要を構築、`primary_source` を欠損マーク |
| API レート制限 | 指数バックオフでリトライ、代替ソースへフォールバック |
| 矛盾する情報 | 両論併記、信頼度の高いソースを優先表示 |
| トピックが曖昧 | 候補を列挙してユーザーに確認 |

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

facts:
  origin:
    description: "室町時代末期に成立したとされる日本の昔話。最古の文献は..."
    sources: ["国文学研究資料館", "Wikipedia"]
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
  cultural:
    - aspect: "桃の呪術的意味"
      description: "中国由来の桃信仰。邪気を払う霊果とされた"
      source: "日本民俗学会誌"

connections:
  related_works:
    - title: "桃太郎（芥川龍之介）"
      type: "小説"
      relation: "鬼の視点から再解釈したパロディ"

trivia:
  - fact: "岡山県には桃太郎神社が実在する"
    source: "岡山県観光連盟"
```
