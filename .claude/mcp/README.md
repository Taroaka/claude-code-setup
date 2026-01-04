# MCP Server 設定

このディレクトリには、プロジェクト固有のMCPサーバー設定が含まれています。

## Chrome DevTools MCP

Chrome DevTools MCPは約17,000トークンを消費するため、必要な時だけ使用することを推奨します。

### 使用方法

Chrome DevTools MCPを有効にしてClaude Codeを起動：

```bash
claude --mcp-config .claude/mcp/chrome-devtools.json
```

### 含まれる機能（26ツール）

- ページナビゲーション、スクリーンショット、要素操作
- ネットワークリクエストの監視
- パフォーマンス分析
- JavaScriptの実行
- フォームの自動入力
- その他ブラウザ自動化機能

### 注意事項

- このMCPサーバーは通常のセッションには含まれていません
- 必要な時だけ `--mcp-config` オプションで起動してください
- コンテキストウィンドウを約17,000トークン消費します
