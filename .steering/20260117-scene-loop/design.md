# Scene-level Loop Design (Task 9)

## 目的
シーン単位での生成とレビューを反復し、**整合性のある脚本**を構築する。

## 参照
- `.steering/20260117-scene-loop/requirements.md`
- `docs/script-creation.md`
- `docs/story-creation.md`

## 位置づけ
- SCRIPTステージ内のサブグラフとして動作
- シーンは **順序依存** のため直列処理

## Scene Plan（設計単位）

最低限のシーン計画オブジェクトは以下を含む：

```yaml
scene_plan:
  scene_id: 1
  purpose: "視聴者の注意を引く"
  duration_seconds: 6
  key_beats:
    - "主人公が問題意識を持つ"
  visual_notes:
    - "朝の室内、静かな光"
  audio_notes:
    - "低めのBGM、落ち着いたナレーション"
```

## フロー

```
ScenePlan → DraftScene → ReviewScene → (ReviseScene)* → Accept → Append
```

### 1) DraftScene
- 入力: Scene Plan + 前後のコンテキスト + グローバル制約
- 出力: シーン台本（script.mdの該当シーン相当）

### 2) ReviewScene
- 入力: シーン草稿 + 前後の要約
- 出力: `accept | revise` + 理由
- 観点:
  - 前後の脈絡
  - 世界観/キャラ/トーン
  - 制約（尺/言語/形式）遵守

### 3) ReviseScene
- 修正理由に応じて再提出
- **最大2回**まで
- 超過時は **人間ゲート**へ昇格

### 4) Accept / Append
- acceptされたシーンのみ統合
- 統合時にタイムラインを更新

## 統合ルール（script.md）

- `script.md` は **scene_id順** に並べる
- タイムラインは `duration_seconds` をもとに更新
- 視覚/音声の指示（asset hint）を含める

## 状態管理（state.txt）

シーン状態は `state.txt` に追記で記録：

```
runtime.scene.1.status=draft|review|revise|accepted|failed
runtime.scene.1.attempts=0
```

## 失敗時の扱い

- **非整合**（矛盾/世界観逸脱）は revise
- **制約違反**（尺/形式/禁止事項）は revise
- **反復失敗**は人間レビューゲートへ

## 受け入れ条件

- Scene Plan → Draft → Review → Revise → Accept の流れが明文化されている
- 反復回数とゲート条件が明確
- `script.md` 統合規則が記載されている
