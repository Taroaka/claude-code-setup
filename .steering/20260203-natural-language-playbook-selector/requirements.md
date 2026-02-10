# Requirements: Natural Language Playbook Selector

## Goal
- ユーザーが ID 指定ではなく自然言語で「やり方 × 3（調査/台本/シーン生成）」を指定できるようにする。

## Required behavior
- 3カテゴリそれぞれから 1つずつ方式を選ぶ
- 推薦ロジックは持たず、ユーザー指定を優先する
- 曖昧な場合のみ不足カテゴリを確認する

## Constraints
- コード実装は不要（md運用で実現）

