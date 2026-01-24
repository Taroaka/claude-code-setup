# Scene-level Loop Requirements (Task 9)

## 目的
シーン単位での生成・レビュー・再提出のループを標準化し、
脚本の品質と一貫性を担保する。

## 参照
- `docs/script-creation.md`
- `docs/story-creation.md`
- `.steering/20260117-langgraph-topology/design.md`

## スコープ
- シーン計画オブジェクトの定義
- Scriptwriter → Reviewer の反復
- 失敗時の再提出・人間ゲートへの昇格
- 受理済みシーンの統合規則

## 前提
- シーンは順序依存のため **直列処理**
- `script.md` は最終統合成果物

## 要件

### シーン計画（Scene Plan）
以下の項目を持つこと：
- scene_id
- purpose
- duration_seconds
- key_beats
- visual_notes
- audio_notes

### 反復フロー
- Scriptwriter が1シーンを生成
- Reviewer が accept / revise を返す
- revise の場合、Scriptwriter が再提出
- 再提出は最大2回まで（超過時は人間ゲート）

### 統合
- accept されたシーンのみを `script.md` に統合
- タイムラインと整合すること

## 受け入れ条件
- シーン計画と反復フローが明記されている
- 人間ゲートへの昇格条件が定義されている
