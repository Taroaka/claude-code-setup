# 情報収集手順書

**最終更新**: 2026-01-05
**対象システム**: TikTok Story Creator (ToC)
**対象読者**: AIエージェント（情報収集モジュール）

このドキュメントは、AIエージェントが物語生成のための情報を収集する際の手順を定義します。

---

## 📋 目次

1. [情報収集の目的](#情報収集の目的)
2. [収集対象の情報種別](#収集対象の情報種別)
3. [情報源](#情報源)
4. [収集手順](#収集手順)
5. [データ品質基準](#データ品質基準)
6. [出力フォーマット](#出力フォーマット)
7. [エラーハンドリング](#エラーハンドリング)

---

## 情報収集の目的

TikTok向けの1分動画に適した**魅力的で共感を呼ぶ物語の素材**を収集すること。

### 重要な観点
- **バイラル性**: 拡散されやすいトピック
- **感情的インパクト**: 感動、驚き、共感を生む要素
- **トレンド性**: 現在注目されているテーマ
- **短尺適性**: 1分で伝えられる情報量

---

## 収集対象の情報種別

### 1. トレンドトピック
**目的**: 現在バズっているテーマを把握

**収集内容**:
- SNSトレンド（Twitter/X、TikTok、Reddit）
- Google Trends上位キーワード
- ニュースで話題のトピック
- 季節イベント・記念日

**例**:
- 「AI技術の最新進化」
- 「宇宙探査の新発見」
- 「感動的な動物の救助劇」

---

### 2. ニュース・時事ネタ
**目的**: 最新の出来事を物語化

**収集内容**:
- 科学技術ニュース
- 人間関係のドラマ
- 社会問題（ただしセンシティブなトピックは避ける）
- ポジティブなニュース（希望、成功、革新）

**避けるべきトピック**:
- 政治的に偏ったテーマ
- 暴力的・悲惨すぎる事件
- 特定の宗教・民族に関する問題
- 過度にセンシティブな内容

---

### 3. 知識・雑学
**目的**: 「知らなかった！」という驚きを提供

**収集内容**:
- 科学的な面白い事実
- 歴史上の意外なエピソード
- 身近な物の起源
- ライフハック・豆知識

**例**:
- 「ハチミツは腐らない理由」
- 「人間の体内には100兆の細菌がいる」
- 「宇宙で最も静かな場所」

---

### 4. 感動的ストーリー
**目的**: 視聴者の心を動かす

**収集内容**:
- 困難を乗り越えた実話
- 人間と動物の絆
- 小さな親切・善行
- 夢を実現した人の物語

---

### 5. 意外性・パラドックス
**目的**: 「え、そうなの？」という驚き

**収集内容**:
- 直感に反する事実
- 思い込みを覆す情報
- 科学的パラドックス
- 比較による意外な対比

**例**:
- 「飛行機は実は安全な乗り物トップ3」
- 「クジラの心臓は車と同じサイズ」

---

## 情報源

### 推奨情報源（API利用可能）

#### 1. ニュースAPI
- **NewsAPI** (https://newsapi.org/)
  - カテゴリ: `technology`, `science`, `health`, `entertainment`
  - 言語: `ja`, `en`
  - 取得件数: 最新20件

- **Google News RSS**
  - カテゴリ別フィード取得

#### 2. トレンドAPI
- **Google Trends API** (非公式)
  - 日本のトレンドキーワード上位10件
  - カテゴリ: すべて

- **Twitter/X API** (v2)
  - トレンドトピック取得
  - ハッシュタグ分析

#### 3. Reddit API
- **r/todayilearned** - 興味深い事実
- **r/science** - 科学ニュース
- **r/UpliftingNews** - ポジティブなニュース
- **r/interestingasfuck** - 意外な情報

#### 4. Wikipedia API
- **Wikimedia REST API**
  - 日本語版のトレンド記事
  - 特定トピックの詳細情報取得

#### 5. Open Data Sources
- **NASA API** - 宇宙関連情報
- **The Cat API** - 動物コンテンツ
- **Open Library API** - 書籍・知識

---

### 補助的な情報源（必要に応じて）

- **YouTube トレンド** - 動画トレンド分析
- **TikTok Creative Center** - TikTokトレンド分析
- **Hacker News API** - 技術トレンド

---

## 収集手順

### ステップ1: テーマの決定

**入力**:
- ユーザー指定のテーマ（オプション）
- 自動トレンド収集（デフォルト）

**処理**:
```python
# テーマが指定されていない場合、トレンドから自動選択
if user_theme:
    theme = user_theme
else:
    trends = fetch_google_trends(country='JP', limit=10)
    theme = select_most_suitable_trend(trends)
```

**判断基準**（トレンド選択時）:
- バイラル性スコア > 7/10
- センシティブ度 < 3/10
- 物語化可能性 > 6/10

---

### ステップ2: 関連情報の収集

**処理フロー**:
```
1. テーマに関連するニュース記事を5-10件取得
2. Wikipedia でテーマの背景情報を取得
3. Reddit で関連する興味深い投稿を3-5件取得
4. 必要に応じて専門API（NASA、科学系等）から詳細情報を取得
```

**具体例**:

テーマが「AI技術の進化」の場合：

```python
# 1. ニュース取得
news = fetch_news_api(
    query='AI artificial intelligence',
    category='technology',
    language='ja',
    limit=10,
    from_date='last_7_days'
)

# 2. Wikipedia情報取得
wiki_data = fetch_wikipedia(
    title='人工知能',
    language='ja'
)

# 3. Reddit投稿取得
reddit_posts = fetch_reddit(
    subreddit='artificial',
    sort='hot',
    limit=5,
    time_filter='week'
)

# 4. 統合
all_sources = {
    'news': news,
    'wiki': wiki_data,
    'reddit': reddit_posts,
    'collected_at': datetime.now()
}
```

---

### ステップ3: 情報のフィルタリング

**除外基準**:
- [ ] センシティブなコンテンツ（暴力、政治、宗教）
- [ ] 広告・宣伝目的の記事
- [ ] 信頼性が低い情報源
- [ ] 古すぎる情報（2週間以上前）
- [ ] 重複コンテンツ

**品質スコアリング**:
```python
def calculate_quality_score(source):
    score = 0

    # 信頼性（最大30点）
    if source.domain in TRUSTED_DOMAINS:
        score += 30

    # 新鮮度（最大20点）
    age_days = (datetime.now() - source.published_date).days
    if age_days <= 1:
        score += 20
    elif age_days <= 7:
        score += 15
    elif age_days <= 14:
        score += 10

    # エンゲージメント（最大30点）
    engagement = source.likes + source.shares + source.comments
    if engagement > 10000:
        score += 30
    elif engagement > 1000:
        score += 20
    elif engagement > 100:
        score += 10

    # コンテンツの長さ（最大20点）
    word_count = len(source.content.split())
    if 300 <= word_count <= 1500:
        score += 20
    elif 150 <= word_count < 300:
        score += 15
    elif word_count < 150:
        score += 5

    return score

# スコア70点以上の情報源のみ保持
filtered_sources = [s for s in all_sources if calculate_quality_score(s) >= 70]
```

---

### ステップ4: 情報の要約と構造化

**処理**:
各情報源から重要な要素を抽出：

```python
structured_data = {
    'theme': theme,
    'main_topic': extract_main_topic(filtered_sources),
    'key_facts': extract_key_facts(filtered_sources, limit=5),
    'emotional_elements': extract_emotional_elements(filtered_sources),
    'surprising_facts': extract_surprising_facts(filtered_sources),
    'human_interest': extract_human_interest(filtered_sources),
    'sources': [
        {
            'url': source.url,
            'title': source.title,
            'summary': source.summary,
            'published_date': source.published_date,
            'reliability_score': source.reliability
        }
        for source in filtered_sources
    ],
    'collected_at': datetime.now(),
    'total_sources': len(filtered_sources)
}
```

---

### ステップ5: データベースへの保存

**保存先テーブル**: `information_sources`

```python
# データベース保存
story_id = create_story_placeholder()  # 後で物語生成時に使用

for source in structured_data['sources']:
    save_to_db(
        table='information_sources',
        data={
            'story_id': story_id,
            'source_type': source['type'],
            'source_url': source['url'],
            'raw_data': json.dumps(source),
            'collected_at': datetime.now()
        }
    )
```

**参考**: docs/DATABASE_DESIGN.md

---

## データ品質基準

### 最低基準（必須）

- [ ] 情報源が最低3件以上
- [ ] すべての情報源の信頼性スコア > 50/100
- [ ] テーマの明確性 > 7/10
- [ ] センシティブコンテンツが含まれていない
- [ ] 物語化可能な要素（感情、驚き、知識）が1つ以上存在

### 推奨基準

- [ ] 情報源が5件以上
- [ ] 平均信頼性スコア > 70/100
- [ ] 複数の情報源タイプ（ニュース + Wiki + Reddit等）
- [ ] 感情的要素と知的要素のバランスが取れている

---

## 出力フォーマット

### JSON構造

```json
{
  "collection_id": "uuid-here",
  "theme": "AI技術の進化と人間社会への影響",
  "collection_date": "2026-01-05T12:00:00Z",
  "sources": [
    {
      "source_id": "uuid-here",
      "type": "news",
      "title": "ChatGPTが医療診断で人間の医師を超えた",
      "url": "https://example.com/news/...",
      "summary": "最新の研究により、AIが特定の医療診断で...",
      "published_date": "2026-01-04",
      "reliability_score": 85,
      "engagement": {
        "likes": 15000,
        "shares": 3000,
        "comments": 500
      }
    }
  ],
  "extracted_elements": {
    "key_facts": [
      "AIの診断精度が95%に到達",
      "人間の医師の平均精度は87%",
      "誤診リスクが40%減少"
    ],
    "emotional_hooks": [
      "AIによって命を救われた患者の実話",
      "医師たちの複雑な感情"
    ],
    "surprising_facts": [
      "AIは医師の仕事を奪うのではなく、補完する",
      "診断時間が平均60%短縮"
    ]
  },
  "quality_metrics": {
    "overall_score": 82,
    "source_count": 7,
    "average_reliability": 78,
    "theme_clarity": 9,
    "story_potential": 8
  }
}
```

---

## エラーハンドリング

### 一般的なエラーと対処法

#### Error 1: API接続失敗

**症状**: NewsAPI、Google Trends等のAPI接続エラー

**対処法**:
```python
try:
    news = fetch_news_api(query, limit=10)
except APIConnectionError as e:
    # フォールバック: 別のAPI or キャッシュデータを使用
    logger.warning(f"NewsAPI failed: {e}. Using fallback source.")
    news = fetch_alternative_news_source(query)
except RateLimitError:
    # レート制限に達した場合は待機
    logger.info("Rate limit reached. Waiting 60 seconds...")
    time.sleep(60)
    news = fetch_news_api(query, limit=10)
```

---

#### Error 2: 情報源が不足

**症状**: フィルタリング後に情報源が3件未満

**対処法**:
```python
if len(filtered_sources) < 3:
    # 基準を緩和して再試行
    logger.warning("Insufficient sources. Relaxing quality threshold.")
    filtered_sources = [s for s in all_sources if calculate_quality_score(s) >= 50]

    if len(filtered_sources) < 3:
        # それでも不足なら、別のテーマを試す
        raise InformationGatheringError(
            "Cannot gather sufficient information for this theme. "
            "Consider trying a different theme."
        )
```

---

#### Error 3: センシティブコンテンツの検出

**症状**: 不適切なコンテンツがフィルタリングをすり抜けた

**対処法**:
```python
# センシティブワードチェック
SENSITIVE_KEYWORDS = [
    '暴力', '戦争', '死', '政治', '宗教',
    'violence', 'death', 'politics', 'religion'
]

def contains_sensitive_content(text):
    text_lower = text.lower()
    for keyword in SENSITIVE_KEYWORDS:
        if keyword in text_lower:
            return True
    return False

# 最終チェック
if contains_sensitive_content(structured_data['main_topic']):
    logger.error("Sensitive content detected. Rejecting this theme.")
    raise SensitiveContentError("This theme contains sensitive material.")
```

---

#### Error 4: 品質基準未達

**症状**: 収集した情報の品質スコアが低すぎる

**対処法**:
```python
if structured_data['quality_metrics']['overall_score'] < 60:
    # 再収集を試みる（最大3回）
    for attempt in range(3):
        logger.info(f"Quality too low. Retry attempt {attempt + 1}/3")
        structured_data = collect_information(theme)
        if structured_data['quality_metrics']['overall_score'] >= 60:
            break
    else:
        # 3回試してもダメなら別のテーマへ
        raise QualityThresholdError(
            "Unable to meet quality standards for this theme."
        )
```

---

## 実装チェックリスト

情報収集モジュールを実装する際の確認事項：

- [ ] すべての推奨情報源APIの接続テスト完了
- [ ] センシティブコンテンツフィルターが機能している
- [ ] 品質スコアリングロジックが実装されている
- [ ] データベース保存が正常に動作する
- [ ] エラーハンドリングが適切に実装されている
- [ ] ログ記録が適切に行われている
- [ ] 出力JSONフォーマットが仕様に準拠している
- [ ] ユニットテストが80%以上のカバレッジを達成

---

## 関連ドキュメント

- **docs/story-creation.md** - 物語生成手順書（次のステップ）
- **docs/DATABASE_DESIGN.md** - データベース設計
- **CLAUDE-patterns.md** - コードパターンと規約
- **CLAUDE-decisions.md** - アーキテクチャ決定記録（ADR）

---

## 更新履歴

| 日付 | 変更内容 | 担当者 |
|------|---------|--------|
| 2026-01-05 | 初版作成 | Claude Code |

---

**次のステップ**: この手順書を参照して、`src/agents/information_gatherer.py` を実装してください。
