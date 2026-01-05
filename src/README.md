# src/ - ソースコードディレクトリ

このディレクトリには、TikTok Story Creator (ToC) のすべてのソースコードが格納されます。

## ディレクトリ構造

```
src/
├── agents/          # AIエージェント（情報収集、物語生成）
├── generators/      # マルチメディア生成（音声、画像、動画）
│   ├── audio/      # 音声合成
│   ├── image/      # 画像生成
│   └── video/      # 動画生成AI
├── database/        # DB接続とモデル
├── renderer/        # 動画レンダリング（FFmpeg/MoviePy）
└── utils/           # 共通ユーティリティ
```

## モジュール説明

### agents/
AIエージェントの実装を格納します。

**主要ファイル（予定）**:
- `information_gatherer.py` - 情報収集エージェント（docs/information-gathering.md を参照）
- `story_generator.py` - 物語生成エージェント（docs/story-creation.md を参照）

### generators/
マルチメディア生成機能を格納します。

**サブディレクトリ**:
- `audio/` - 音声合成（ElevenLabs, OpenAI TTS, Google TTS）
- `image/` - 画像生成（DALL-E 3, Stable Diffusion 3.5）
- `video/` - 動画生成AI（Veo 3.1, Sora 2, Kling, Runway, Pika）

### database/
データベース接続とモデル定義を格納します。

**主要ファイル（予定）**:
- `models.py` - SQLAlchemy モデル（videos, stories, information_sources, video_generation_logs）
- `connection.py` - PostgreSQL接続管理

**参考**: docs/DATABASE_DESIGN.md

### renderer/
動画レンダリング機能を格納します。

**主要ファイル（予定）**:
- `video_composer.py` - FFmpeg/MoviePyを使った動画合成

### utils/
共通ユーティリティ関数を格納します。

**主要ファイル（予定）**:
- `config_loader.py` - YAML設定ファイルの読み込み
- `api_key_manager.py` - APIキー管理（Pattern 8参照）
- `logger.py` - ログ設定（Pattern 10参照）
- `exceptions.py` - カスタム例外クラス（Pattern 9参照）

## 開発ガイドライン

### インポート規約

```python
# 標準ライブラリ
import os
from typing import Optional, List

# サードパーティライブラリ
import yaml
from sqlalchemy import create_engine

# プロジェクト内インポート
from src.database.models import Video, Story
from src.utils.api_key_manager import APIKeyManager
```

### 型ヒント必須

すべてのパブリック関数には型ヒントを付与してください（Pattern 3参照）。

### ドキュメント

関数には必ずdocstringを記載してください。

```python
def generate_story(theme: str, sources: List[Dict[str, Any]]) -> Optional[str]:
    """物語を生成する

    Args:
        theme: 物語のテーマ
        sources: 情報ソースのリスト

    Returns:
        生成された物語（失敗時はNone）
    """
    pass
```

## 関連ドキュメント

- **CLAUDE-patterns.md** - コードパターンと規約
- **CLAUDE-decisions.md** - アーキテクチャ決定記録
- **DATABASE_DESIGN.md** - データベース設計
