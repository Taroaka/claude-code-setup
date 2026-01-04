#!/bin/bash

# 手動レビューファイル生成スクリプト
# 使用法: ./scripts/review-pr.sh <task-name>

set -e

# 引数チェック
if [ $# -eq 0 ]; then
    echo "使用法: $0 <task-name>"
    echo "例: $0 initial-project-structure"
    exit 1
fi

TASK_NAME=$1
DATE=$(date +%Y-%m-%d)
REVIEW_FILE="workflow/reviews/${DATE}_${TASK_NAME}_review.md"

# テンプレートファイルの存在確認
if [ ! -f "workflow/review-template.md" ]; then
    echo "エラー: workflow/review-template.md が見つかりません"
    exit 1
fi

# レビューディレクトリの作成
mkdir -p workflow/reviews

# テンプレートからレビューファイルを作成
cp workflow/review-template.md "$REVIEW_FILE"

# タスクIDとファイル名を更新
sed -i.bak "s/YYYY-MM-DD/${DATE}/g" "$REVIEW_FILE"
sed -i.bak "s/\[short-name\]/${TASK_NAME}/g" "$REVIEW_FILE"
sed -i.bak "s/\[タスク名\]/タスク: ${TASK_NAME}/g" "$REVIEW_FILE"
rm -f "${REVIEW_FILE}.bak"

echo "✅ レビューファイルを作成しました: $REVIEW_FILE"
echo ""
echo "次のステップ:"
echo "1. レビューファイルを編集して、レビュー内容を記入"
echo "2. AIにレビューを依頼: \"${REVIEW_FILE} を使ってコードレビューしてください\""
echo ""
echo "レビューファイルを開くには:"
echo "  code $REVIEW_FILE"
