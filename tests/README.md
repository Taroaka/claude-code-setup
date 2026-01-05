# tests/ - テストディレクトリ

このディレクトリには、TikTok Story Creator (ToC) のすべてのテストが格納されます。

## テスト構造（予定）

```
tests/
├── unit/                  # ユニットテスト
│   ├── test_agents/       # エージェントのテスト
│   ├── test_generators/   # 生成機能のテスト
│   ├── test_database/     # データベースのテスト
│   └── test_utils/        # ユーティリティのテスト
├── integration/           # 統合テスト
├── fixtures/              # テストデータ
└── conftest.py            # pytest設定とfixtures
```

## テストフレームワーク

**使用ツール**:
- **pytest** - テストフレームワーク
- **pytest-cov** - カバレッジ測定
- **pytest-mock** - モック機能
- **pytest-asyncio** - 非同期テスト（必要に応じて）

## テストパターン

### ユニットテスト例

```python
# tests/unit/test_agents/test_story_generator.py

import pytest
from src.agents.story_generator import StoryGenerator

@pytest.fixture
def story_generator():
    """StoryGeneratorのfixtureを作成"""
    return StoryGenerator(provider='mock')

def test_generate_story_success(story_generator):
    """物語生成が成功する場合のテスト"""
    theme = "科学技術"
    sources = [{"url": "https://example.com", "content": "AI進化"}]

    result = story_generator.generate(theme, sources)

    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0

def test_generate_story_empty_sources(story_generator):
    """情報ソースが空の場合のテスト"""
    theme = "科学技術"
    sources = []

    with pytest.raises(ValueError):
        story_generator.generate(theme, sources)
```

**参考**: CLAUDE-patterns.md - Pattern 11

---

### モック例

```python
# tests/unit/test_generators/test_video/test_veo_client.py

import pytest
from unittest.mock import Mock, patch
from src.generators.video.veo_client import VeoVideoGenerator

@pytest.fixture
def mock_veo_api():
    """Veo APIをモック化"""
    with patch('src.generators.video.veo_client.VeoAPI') as mock:
        mock.return_value.generate_video.return_value = {
            'video_url': 'https://example.com/video.mp4',
            'status': 'completed'
        }
        yield mock

def test_generate_video_success(mock_veo_api):
    """動画生成が成功する場合のテスト"""
    generator = VeoVideoGenerator(api_key='test_key')
    result = generator.generate(prompt="テスト動画", duration=60)

    assert result['status'] == 'completed'
    assert 'video_url' in result
```

---

### データベーステスト例

```python
# tests/unit/test_database/test_models.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, Video, Story

@pytest.fixture
def db_session():
    """テスト用DBセッション"""
    engine = create_engine('postgresql://test:test@localhost/test_db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    Base.metadata.drop_all(engine)

def test_create_video(db_session):
    """動画レコード作成のテスト"""
    video = Video(
        title="テスト動画",
        file_path="/tmp/test.mp4",
        duration_seconds=60,
        status="pending"
    )
    db_session.add(video)
    db_session.commit()

    assert video.id is not None
    assert video.title == "テスト動画"
    assert video.aspect_ratio == "9:16"  # デフォルト値
```

**参考**: CLAUDE-patterns.md - Pattern 11

---

## テスト実行

### 全テスト実行
```bash
pytest
```

### カバレッジ付き実行
```bash
pytest --cov=src --cov-report=html
```

### 特定のテストファイルのみ
```bash
pytest tests/unit/test_agents/test_story_generator.py
```

### 特定のテスト関数のみ
```bash
pytest tests/unit/test_agents/test_story_generator.py::test_generate_story_success
```

### マーカーを使った実行
```python
# テストにマーカーを付与
@pytest.mark.slow
def test_long_running_task():
    pass

# slowマーカーのテストをスキップ
pytest -m "not slow"
```

---

## テストカバレッジ目標

- **全体**: 80%以上
- **重要なモジュール（agents, database）**: 90%以上
- **ユーティリティ**: 70%以上

---

## CI/CD統合

GitHub Actionsでテストを自動実行する予定：

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --cov=src --cov-report=xml
```

---

## テスト作成ガイドライン

1. **命名規約**: `test_<module>_<function>_<scenario>`
   - 例: `test_story_generator_generate_success`

2. **AAA パターン**:
   - Arrange（準備）
   - Act（実行）
   - Assert（検証）

3. **1テスト1検証**: 各テストは1つの機能のみを検証

4. **モック化**: 外部依存（API、DB）は必ずモック化

5. **テストデータ**: `tests/fixtures/` に保存

---

## 関連ドキュメント

- **CLAUDE-patterns.md** - Pattern 11（テストパターン）
- **CLAUDE-decisions.md** - アーキテクチャ決定記録
