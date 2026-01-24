# Scene-level Loop（正本）

このドキュメントは `.steering/20260117-scene-loop/` で合意した内容を **恒久仕様として昇華**したもの。

## 目的

シーン単位で生成→レビュー→再提出を反復し、整合性のある `script.md` を構築する。

## Scene Plan（最小）

- `scene_id`
- `purpose`
- `duration_seconds`
- `key_beats`
- `visual_notes`
- `audio_notes`

## フロー

`ScenePlan → DraftScene → ReviewScene → (ReviseScene)* → Accept → Append`

### 反復上限

- revise は最大2回
- 超過時は人間ゲートへ昇格

## 統合規則

- accept 済みシーンのみ `script.md` に統合
- `scene_id` の順序で並べる

## 状態記録

`state.txt` に追記:

- `runtime.scene.<id>.status=draft|review|revise|accepted|failed`
- `runtime.scene.<id>.attempts=<n>`

## 参照

- `docs/script-creation.md`
- `docs/story-creation.md`
