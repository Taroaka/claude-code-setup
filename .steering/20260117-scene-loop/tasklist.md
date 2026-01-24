# Scene-level Loop Tasklist (Task 9)

## 仕様整理（Spec）

### 入出力
- **入力**: `story.md`（シーン計画の根拠）, 直前シーン要約, 制約（言語/尺/比率）
- **出力**: `script.md`（シーン詳細を順序通りに統合）
- **状態管理**: `output/<topic>_<timestamp>/state.txt` に追記型で記録

### 主要オブジェクト
- **Scene Plan**（最小要素）
  - `scene_id`, `purpose`, `duration_seconds`, `key_beats`, `visual_notes`, `audio_notes`
- **Scene Draft**
  - narrative / visual / audio / text_overlay / timing
- **Review Result**
  - `decision=accept|revise`
  - `reasons[]`

### 反復条件
- `revise` の場合は再提出
- 最大2回まで（3回目で人間ゲート）
- 失敗理由は `state.txt` に記録

### 統合ルール
- acceptされたシーンのみ `script.md` に追記
- `scene_id` の順序で整列
- 時間配分が崩れた場合は `revise` を優先

---

## 実装タスク

### 1) シーン計画の生成・保持
- [ ] `story.md` から Scene Plan を抽出する処理を設計
- [ ] Scene Plan を `state.txt` に記録する形式を定義
- [ ] Scene Plan の最小必須項目のバリデーションを実装

### 2) シーン作成（Draft）
- [ ] Scriptwriter に Scene Plan + 前後文脈 + 制約を渡す
- [ ] `script.md` に準拠したシーン草稿を生成
- [ ] 草稿に `scene_id` と `duration_seconds` を含める

### 3) シーンレビュー
- [ ] Reviewer に「前後の脈絡」「制約遵守」「世界観整合」を評価させる
- [ ] `accept|revise` の判定と理由を返す
- [ ] 判定結果を `state.txt` に追記

### 4) 再提出ループ
- [ ] revise の場合は修正理由を Scriptwriter に返す
- [ ] 最大2回までの再提出カウンタを管理
- [ ] 超過時に人間ゲートへエスカレーション

### 5) 統合
- [ ] accept 済みシーンのみ `script.md` に統合
- [ ] タイムライン整合（duration合計）が取れているか検証
- [ ] 不整合時は該当シーンを revise へ戻す

### 6) ログと状態
- [ ] `state.txt` に以下を追記：
  - `runtime.scene.<id>.status`
  - `runtime.scene.<id>.attempts`
  - `last_error`
- [ ] 途中停止時は最後のブロックから再開

---

## 完了条件

- Scene Plan → Draft → Review → Revise → Accept の流れが実装されている
- `state.txt` の追記によって進捗が再現できる
- `script.md` が scene_id順で整合的に統合される
