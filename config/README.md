# config/ - 設定ファイルディレクトリ

このディレクトリには、TikTok Story Creator (ToC) の設定ファイルが格納されます。

## 設定ファイル一覧（予定）

### providers.yaml
AIプロバイダーの設定と切替を管理します。

**構造例**:
```yaml
llm:
  active: openai  # 'openai' or 'claude'
  openai:
    model: gpt-5.2
    temperature: 0.7
    max_tokens: 2000
  claude:
    model: claude-4.0-sonnet
    temperature: 0.7
    max_tokens: 2000

audio:
  active: elevenlabs  # 'elevenlabs', 'openai_tts', 'google_tts'
  elevenlabs:
    voice_id: "21m00Tcm4TlvDq8ikWAM"
    model: "eleven_multilingual_v2"
  openai_tts:
    model: "tts-1-hd"
    voice: "alloy"
  google_tts:
    language_code: "ja-JP"
    voice_name: "ja-JP-Wavenet-A"

image:
  active: dalle3  # 'dalle3', 'stable_diffusion'
  dalle3:
    model: "dall-e-3"
    size: "1024x1792"
    quality: "hd"
  stable_diffusion:
    model: "stable-diffusion-3.5"
    steps: 50

video:
  active: veo  # 'veo', 'sora', 'kling', 'runway', 'pika', 'stable_video'
  veo:
    model: "veo-3.1"
    resolution: "1080x1920"
    fps: 30
  sora:
    model: "sora-2"
    resolution: "1080x1920"
    duration: 60
```

**参考**: CLAUDE-decisions.md - ADR-002, ADR-008

---

### video_settings.yaml
動画生成の詳細設定を管理します。

**構造例**:
```yaml
video:
  aspect_ratio: "9:16"
  resolution:
    width: 1080
    height: 1920
  fps: 30
  duration: 60  # 秒
  format: "mp4"
  codec: "h264"
  bitrate: "5M"

audio:
  sample_rate: 44100
  channels: 2
  codec: "aac"
  bitrate: "192k"

subtitles:
  enabled: true
  font: "Arial"
  font_size: 48
  color: "white"
  position: "bottom"
  background: true
  background_color: "black"
  background_opacity: 0.5

effects:
  fade_in: 0.5  # 秒
  fade_out: 0.5  # 秒
  transitions: true
```

---

## 環境変数との分離

**YAML設定ファイル（このディレクトリ）**:
- プロバイダー選択
- モデルパラメータ
- 動画設定

**環境変数（.env）**:
- APIキー（シークレット）
- データベース接続情報（シークレット）

**理由**: シークレットをコードや設定ファイルに含めないため（ADR-008参照）

## 使用方法

### Pythonからの読み込み

```python
import yaml

# プロバイダー設定の読み込み
with open('config/providers.yaml') as f:
    providers = yaml.safe_load(f)

llm_provider = providers['llm']['active']
llm_config = providers['llm'][llm_provider]

# 動画設定の読み込み
with open('config/video_settings.yaml') as f:
    video_settings = yaml.safe_load(f)

resolution = video_settings['video']['resolution']
```

**参考**: CLAUDE-patterns.md - Pattern 2

## Gitでの管理

- ✅ **コミット対象**: `providers.yaml`, `video_settings.yaml`
- ❌ **コミット除外**: シークレットを含むファイル（存在しない）

## 関連ドキュメント

- **CLAUDE-patterns.md** - Pattern 2（設定ファイル管理）
- **CLAUDE-decisions.md** - ADR-002（マルチプロバイダー）、ADR-008（YAML設定）
