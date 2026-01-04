# Claude Code セットアップ - やるべきこと

このリポジトリをクローンした後にやるべきことをまとめました。

## 必須ステップ

### 1. ファイルのコピーと配置
- [x] このGitHubリポジトリ内のファイルをプロジェクトディレクトリ（意図したコードベースがある場所）にコピーする

### 2. テンプレートファイルの修正
- [x] テンプレートファイルとCLAUDE.mdを好みに応じて修正する
- [x] `.claude/settings.json`を確認
  - macOSを使用している場合：Terminal-Notifierをインストール（https://github.com/centminmod/terminal-notifier-setup）
  - macOS以外を使用している場合：`.claude/settings.json`を削除する

### 3. Claude Codeの初回起動と初期化
- [x] プロジェクトディレクトリ内でClaude Codeを初めて起動する
- [x] `/init`コマンドを実行して、Claude Codeにコードベースを分析させ、CLAUDE.mdの指示に従ってメモリバンクシステムファイルを生成させる

## 強く推奨されるステップ

### 4. Visual Studio Codeのインストール
- [x] Visual Studio Codeをインストール
  - 初心者向けYouTube動画ガイド：
    - https://www.youtube.com/watch?v=rPITZvwyoMc
    - https://www.youtube.com/watch?v=P-5bWpUbO60
- [x] Claude Code VSC Extensionをインストール
  - https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code

### 5. GitHub & Gitのセットアップ
- [x] Github.comアカウントにサインアップ
- [x] Visual Studio Code用のGitをインストール
  - YouTubeガイド：
    - https://www.youtube.com/watch?v=twsYxYaQikI
    - https://www.youtube.com/watch?v=z5jZ9lrSpqk

### 6. 高速ツールのインストール（macOS）
- [x] CLAUDE.mdが高速ツールを使用するように更新されているため、以下をインストール：
  ```bash
  brew install ripgrep fd jq
  ```

## オプションステップ

### 7. Dev Containerのセットアップ（オプション）
- [x] Visual Studio Code dev container（Debian 12環境）をセットアップ
  - `.devcontainer/devcontainer.json`を作成
  - 基本的なツール（Node.js, Python, Git, Docker-in-Docker）を含む設定
  - VS Code拡張機能「Dev Containers」のインストールが必要
  - 詳細：https://claude-devcontainers.centminmod.com/

### 8. Git Worktreesの設定
- [x] `.worktreeinclude`ファイルを作成（Claude Desktop appsがGit Worktreesを使用するため）
  - 詳細：https://code.claude.com/docs/en/desktop#claude-code-on-desktop-preview

### 9. Cloudflare/ClerkOS関連ドキュメントの整理
- [x] Cloudflare及びClerkOSプラットフォームを使用する場合：
  - `CLAUDE-cloudflare.md`または`CLAUDE-cloudflare-mini.md`のいずれかを保持
  - `CLAUDE.md`を更新して、選択したファイルを参照
  - 使用しないドキュメントセクションは削除
  - ※使用しないため削除しました

### 10. 参考資料の確認
- [ ] 公式Claude Codeドキュメントを読む：https://docs.anthropic.com/en/docs/claude-code/overview
- [ ] 「Advent of Claude: 31 Days of Claude Code」を読む：https://adocomplete.com/advent-of-claude-2025/

## 前提条件

### Claude AIアカウント
- [ ] 有料のClaude AIアカウントにサインアップ（https://claude.ai/）
  - Claude Pro: $20/月
  - Claude Max: $100/月 または $200/月
  - 各プランには異なる使用量クォータと制限があります
  - 詳細：https://support.anthropic.com/en/articles/9797557-usage-limit-best-practices

## 次のステップ

セットアップが完了したら：
- MCPサーバーのインストールを検討（READMEの「MCP Servers」セクション参照）
- Claude Code Hooks、Subagents、Slash Commandsについて学ぶ
- メモリバンクシステムの活用方法を理解する

## MCPサーバー セットアップ状況

### インストール済み
- ✅ **Context7** - ライブラリドキュメント検索（プラグイン版、自動接続）
- ✅ **Chrome DevTools** - ブラウザ自動化（必要時のみ使用、`.claude/mcp/chrome-devtools.json`）

### スキップ
- ❌ Supabase - 使用しない（PostgreSQL直接使用）
- ❌ Gemini CLI - 不要
- ❌ Notion - 不要
- ❌ Cloudflare Docs - 不要

### Chrome DevTools MCP 使用方法
```bash
claude --mcp-config .claude/mcp/chrome-devtools.json
```
