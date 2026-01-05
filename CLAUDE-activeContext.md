# CLAUDE - Active Context

**最終更新**: 2026-01-05
**プロジェクト**: TikTok Story Creator (ToC)
**現在のフェーズ**: Phase 0 - 初期セットアップ

---

## 🎯 現在のセッション目標

Memory Bank Systemの初期化とプロジェクト基本構造の構築

### 今セッションで達成すること
1. ✅ Memory Bank System ファイルの作成
2. ✅ プロジェクトディレクトリ構造の構築
3. ✅ 基本設定ファイルのテンプレート作成

---

## 📊 プロジェクト概要

**TikTok Story Creator (ToC)** は、AIエージェントが自律的に情報収集し、物語を生成してTikTok向けの縦型動画（1分程度）を自動作成するシステムです。

### システムフロー
```
手動実行トリガー
  ↓
情報収集（docs/information-gathering.md）
  ↓
物語生成（docs/story-creation.md）
  ↓
マルチメディア生成（音声・画像・動画AI）
  ↓
動画レンダリング（FFmpeg/MoviePy）
  ↓
出力: 縦型MP4（9:16, ~1分）
```

---

## ✅ 完了した作業

### セットアップ段階
- ✅ Claude Code基本セットアップ完了
- ✅ Git リポジトリ初期化（ブランチ: claude/determine-next-steps-MzSZL）
- ✅ データベース設計書作成（docs/DATABASE_DESIGN.md）
- ✅ ワークフローテンプレート作成（task-template.md, review-template.md）
- ✅ Git worktree設定（.worktreeinclude）

### ドキュメント
- ✅ README.md - セットアップガイド
- ✅ CLAUDE.md - AIエージェント向けハンドブック
- ✅ DATABASE_DESIGN.md - PostgreSQL スキーマ設計

---

## 🚧 進行中の作業

### 現在のタスク
- 🔄 Memory Bank System 初期化
- 🔄 プロジェクト構造構築（src/, config/, tests/）

---

## 📝 次のステップ（優先順位順）

1. **Phase 1: 手順書の作成**
   - [ ] `docs/information-gathering.md` - 情報収集手順書
   - [ ] `docs/story-creation.md` - 物語生成手順書
   - [ ] `docs/API_SPEC.md` - API仕様書

2. **Phase 2: データベース実装**
   - [ ] PostgreSQL Dockerコンテナ設定
   - [ ] SQLAlchemy モデル実装
   - [ ] マイグレーションスクリプト作成

3. **Phase 3: 情報収集エージェント実装**
   - [ ] トレンド収集モジュール
   - [ ] ニュースAPI統合

4. **Phase 4: 物語生成エンジン実装**
   - [ ] LLM統合（GPT-5.2/Claude 4.0）
   - [ ] プロンプトテンプレート

5. **Phase 5: マルチメディア生成実装**
   - [ ] 音声合成統合
   - [ ] 画像生成統合
   - [ ] 動画生成AI統合

6. **Phase 6: 動画レンダリング実装**
   - [ ] FFmpeg統合
   - [ ] MoviePy実装

---

## 🏗️ プロジェクト構造（計画）

```
tiktok-story-creator/
├── src/
│   ├── agents/              # AIエージェント
│   │   ├── information_gatherer.py
│   │   └── story_generator.py
│   ├── generators/          # マルチメディア生成
│   │   ├── audio/          # 音声合成
│   │   ├── image/          # 画像生成
│   │   └── video/          # 動画生成AI
│   ├── database/           # DB接続とモデル
│   │   ├── models.py
│   │   └── connection.py
│   ├── renderer/           # 動画レンダリング
│   │   └── video_composer.py
│   └── utils/              # ユーティリティ
├── config/                 # 設定ファイル
│   ├── providers.yaml      # AIプロバイダー設定
│   └── video_settings.yaml # 動画生成設定
├── docs/                   # ドキュメント
├── tests/                  # テスト
├── scripts/                # 開発支援スクリプト
├── workflow/               # タスク・レビュー管理
├── .env.example            # 環境変数テンプレート
└── docker-compose.yml      # Docker設定
```

---

## 💡 重要な決定事項

### 技術スタック
- **言語**: Python 3.11+
- **LLM**: OpenAI GPT-5.2 / Claude 4.0 Sonnet（切替可能）
- **音声合成**: ElevenLabs / OpenAI TTS / Google TTS
- **画像生成**: DALL-E 3 / Stable Diffusion 3.5
- **動画生成AI**: Veo 3.1 / Sora 2 / Kling / Runway / Pika / Stable Video
- **動画処理**: FFmpeg, MoviePy
- **データベース**: PostgreSQL 14+
- **インフラ**: Docker/Docker Compose

### アーキテクチャ決定
- 手動実行トリガー（自動化は将来的に検討）
- 手順書ベースのAIエージェント（information-gathering.md, story-creation.md）
- マルチプロバイダー対応（config/providers.yaml で切替）

---

## 🔗 関連ドキュメント

- **CLAUDE.md** - AIエージェント向けハンドブック
- **CLAUDE-patterns.md** - コードパターンと規約
- **CLAUDE-decisions.md** - アーキテクチャ決定記録（ADR）
- **CLAUDE-troubleshooting.md** - トラブルシューティング
- **DATABASE_DESIGN.md** - データベース設計
- **workflow/tasks/** - 実装タスク履歴

---

## 📌 注意事項

### セキュリティ
- `.env` ファイルは絶対にコミットしない
- AI APIキー、DB接続情報はハードコード禁止
- シークレットは環境変数で管理

### 開発プロセス
- タスクは `workflow/tasks/` で管理
- コードレビューは `workflow/review-template.md` を使用
- 小さく安全な変更を心がける

### コード品質
- Linter/Formatter必須（Ruff, Black）
- 型チェック必須（mypy）
- Docker優先のワークフロー

---

## 🎓 学習リソース

- 公式Claude Codeドキュメント: https://docs.anthropic.com/en/docs/claude-code/overview
- Advent of Claude: https://adocomplete.com/advent-of-claude-2025/
