# CLAUDE - Code Patterns & Conventions

**最終更新**: 2026-01-05
**プロジェクト**: TikTok Story Creator (ToC)

このファイルは、プロジェクト内で確立されたコードパターン、規約、ベストプラクティスを記録します。

---

## 📋 目次

1. [プロジェクト規約](#プロジェクト規約)
2. [Pythonコーディング規約](#pythonコーディング規約)
3. [データベースパターン](#データベースパターン)
4. [AI統合パターン](#ai統合パターン)
5. [エラーハンドリング](#エラーハンドリング)
6. [テストパターン](#テストパターン)

---

## プロジェクト規約

### Pattern 1: ディレクトリ構造規約

**コンテキスト**: プロジェクト全体の構造を統一し、可読性と保守性を向上させる

**パターン**:
```
src/
├── agents/          # AIエージェント（情報収集、物語生成）
├── generators/      # マルチメディア生成（音声、画像、動画）
├── database/        # DB接続とモデル
├── renderer/        # 動画レンダリング
└── utils/           # 共通ユーティリティ
```

**理由**:
- 機能別に明確に分離
- 依存関係を明示化
- テストとメンテナンスが容易

**使用例**:
```python
from src.agents.information_gatherer import InformationGatherer
from src.generators.video.veo_client import VeoVideoGenerator
```

---

### Pattern 2: 設定ファイル管理

**コンテキスト**: AIプロバイダーや動画設定を一元管理し、環境変数と分離する

**パターン**:
```
config/
├── providers.yaml         # AIプロバイダー設定（切替可能）
└── video_settings.yaml    # 動画生成パラメータ
```

**理由**:
- 環境変数（.env）はシークレット専用
- YAMLで設定を可読性高く管理
- プロバイダー切替が容易

**使用例**:
```python
import yaml

with open('config/providers.yaml') as f:
    providers = yaml.safe_load(f)

llm_provider = providers['llm']['active']  # 'openai' or 'claude'
```

---

## Pythonコーディング規約

### Pattern 3: 型ヒントの使用

**コンテキスト**: すべてのパブリック関数とメソッドに型ヒントを付与

**パターン**:
```python
from typing import Optional, List, Dict, Any

def generate_story(
    theme: str,
    sources: List[Dict[str, Any]],
    max_length: int = 500
) -> Optional[str]:
    """物語を生成する

    Args:
        theme: 物語のテーマ
        sources: 情報ソースのリスト
        max_length: 最大文字数

    Returns:
        生成された物語（失敗時はNone）
    """
    pass
```

**理由**:
- mypy型チェックが可能
- IDEの補完が効く
- ドキュメントとしても機能

---

### Pattern 4: Linter/Formatter設定

**コンテキスト**: コード品質を自動的に保証

**パターン**:
- **Ruff**: Linter（Flake8, isort, pyupgradeの統合）
- **Black**: Formatter（line-length: 100）
- **mypy**: 型チェック

**pyproject.toml設定例**:
```toml
[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W"]

[tool.black]
line-length = 100

[tool.mypy]
python_version = "3.11"
strict = true
```

**理由**:
- コードスタイルの統一
- バグの早期発見
- レビュー時の指摘削減

---

## データベースパターン

### Pattern 5: SQLAlchemy モデル定義

**コンテキスト**: PostgreSQLテーブルをPythonクラスにマッピング

**パターン**:
```python
from sqlalchemy import Column, String, Text, Integer, TIMESTAMP, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class Video(Base):
    __tablename__ = 'videos'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    file_path = Column(String(500), nullable=False)
    duration_seconds = Column(Integer, nullable=False)
    aspect_ratio = Column(String(10), nullable=False, default='9:16')
    status = Column(String(20), nullable=False, default='pending')
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
```

**理由**:
- タイプセーフなDB操作
- マイグレーションが容易
- リレーション管理が明確

**参考**: docs/DATABASE_DESIGN.md

---

### Pattern 6: データベース接続管理

**コンテキスト**: 環境変数からDB接続を安全に確立

**パターン**:
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://user:password@localhost:5432/tiktok_creator'
)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """DBセッションを取得するジェネレータ"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**理由**:
- 環境変数でシークレット管理
- セッションのライフサイクル管理
- テスト時のモック化が容易

---

## AI統合パターン

### Pattern 7: マルチプロバイダー対応

**コンテキスト**: LLM、音声合成、画像生成、動画生成AIを切替可能にする

**パターン**:
```python
from abc import ABC, abstractmethod
from typing import Optional

class LLMProvider(ABC):
    """LLMプロバイダーの抽象基底クラス"""

    @abstractmethod
    def generate_story(self, prompt: str, **kwargs) -> Optional[str]:
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)

    def generate_story(self, prompt: str, **kwargs) -> Optional[str]:
        response = self.client.chat.completions.create(
            model="gpt-5.2",
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.choices[0].message.content

class ClaudeProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate_story(self, prompt: str, **kwargs) -> Optional[str]:
        response = self.client.messages.create(
            model="claude-4.0-sonnet",
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.content[0].text
```

**理由**:
- プロバイダー切替が容易
- テストが容易（モック化）
- 新しいプロバイダーの追加が簡単

---

### Pattern 8: APIキー管理

**コンテキスト**: 複数のAI APIキーを安全に管理

**パターン**:
```python
import os
from typing import Dict

class APIKeyManager:
    """APIキーを環境変数から取得"""

    @staticmethod
    def get_openai_key() -> str:
        key = os.getenv('OPENAI_API_KEY')
        if not key:
            raise ValueError("OPENAI_API_KEY not set")
        return key

    @staticmethod
    def get_claude_key() -> str:
        key = os.getenv('CLAUDE_API_KEY')
        if not key:
            raise ValueError("CLAUDE_API_KEY not set")
        return key

    @staticmethod
    def get_elevenlabs_key() -> str:
        key = os.getenv('ELEVENLABS_API_KEY')
        if not key:
            raise ValueError("ELEVENLABS_API_KEY not set")
        return key
```

**.env.example**:
```bash
# LLM API Keys
OPENAI_API_KEY=sk-...
CLAUDE_API_KEY=sk-ant-...

# Audio Synthesis
ELEVENLABS_API_KEY=...

# Image Generation
DALL_E_API_KEY=...

# Video Generation
VEO_API_KEY=...
SORA_API_KEY=...
```

**理由**:
- シークレットがコードに含まれない
- 環境別に異なるキーを使用可能
- .gitignoreで.envを除外

---

## エラーハンドリング

### Pattern 9: カスタム例外クラス

**コンテキスト**: エラーの種類を明確にし、適切なハンドリングを可能にする

**パターン**:
```python
class ToCException(Exception):
    """TikTok Story Creatorの基底例外クラス"""
    pass

class InformationGatheringError(ToCException):
    """情報収集失敗"""
    pass

class StoryGenerationError(ToCException):
    """物語生成失敗"""
    pass

class VideoGenerationError(ToCException):
    """動画生成失敗"""
    pass

class DatabaseError(ToCException):
    """データベース操作失敗"""
    pass
```

**使用例**:
```python
try:
    story = generate_story(theme, sources)
except StoryGenerationError as e:
    logger.error(f"Story generation failed: {e}")
    # リトライロジック
```

**理由**:
- エラーの種類が明確
- 適切なリトライ戦略を選択可能
- ログ記録が容易

---

### Pattern 10: ログ記録規約

**コンテキスト**: 構造化ログで問題の診断を容易にする

**パターン**:
```python
import logging
import json
from typing import Any, Dict

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def log_api_call(provider: str, endpoint: str, params: Dict[str, Any]):
    """API呼び出しをログ記録"""
    logger.info(
        "API call",
        extra={
            "provider": provider,
            "endpoint": endpoint,
            "params": json.dumps(params)
        }
    )

def log_error(error: Exception, context: Dict[str, Any]):
    """エラーをコンテキスト付きでログ記録"""
    logger.error(
        f"Error: {str(error)}",
        extra={"context": json.dumps(context)},
        exc_info=True
    )
```

**理由**:
- トラブルシューティングが容易
- パフォーマンス分析が可能
- 本番環境での問題追跡

---

## テストパターン

### Pattern 11: pytest + fixtures

**コンテキスト**: 再利用可能なテストセットアップ

**パターン**:
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def db_session():
    """テスト用DBセッション"""
    engine = create_engine('postgresql://test:test@localhost/test_db')
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def mock_openai_client(monkeypatch):
    """OpenAI APIをモック化"""
    class MockOpenAI:
        def generate_story(self, prompt):
            return "Mock story content"

    monkeypatch.setattr('src.agents.story_generator.openai_client', MockOpenAI())
```

**理由**:
- テストの独立性
- 外部依存のモック化
- セットアップの再利用

---

## 🔄 パターン更新プロセス

新しいパターンが確立されたら：

1. このファイルに追記
2. Pattern番号を連番で付与
3. コンテキスト、パターン、理由、使用例を記載
4. 関連するCLAUDE-decisions.mdのADRを参照

---

## 📚 関連ドキュメント

- **CLAUDE-decisions.md** - アーキテクチャ決定記録
- **CLAUDE-activeContext.md** - 現在のプロジェクト状態
- **DATABASE_DESIGN.md** - データベース設計
