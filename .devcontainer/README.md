# Dev Container セットアップ

このディレクトリには、VS Code Dev Containerの設定が含まれています。

## 前提条件

1. Docker Desktop がインストールされていること
2. Visual Studio Code がインストールされていること
3. VS Code の「Dev Containers」拡張機能がインストールされていること

## 使い方

1. VS Code でこのプロジェクトを開く
2. コマンドパレット（Cmd+Shift+P / Ctrl+Shift+P）を開く
3. "Dev Containers: Reopen in Container" を選択
4. コンテナのビルドが完了するまで待つ

## 含まれるツール

- Node.js (LTS)
- Python (latest)
- Git
- GitHub CLI
- Docker-in-Docker

## Claude Code の設定

ホストマシンの `~/.claude` ディレクトリがコンテナ内にマウントされるため、Claude Code の設定が共有されます。

## トラブルシューティング

コンテナのビルドに失敗した場合：
1. Docker Desktop が起動していることを確認
2. コマンドパレットから "Dev Containers: Rebuild Container" を実行
