# Design: Research 出力量ガイド + production template

## 変更方針

- `workflow/research-template.production.yaml` を追加（厚めの推奨スキーマ）
- `docs/information-gathering.md` に「出力量の目安」を追加
- `.claude/agents/deep-researcher.md` に「最低基準（sources/beat/facts等）」を追加
- `docs/data-contracts.md` で production template の存在を明示

## 量の基準（最低限）

- sources: 12+
- beat sheet: 20+
- scene_plan: 1..20 埋める
- hooks: 10+
- facts: 30+

## 補足

出典が足りない場合は "unverified" として残し、次の探索アクションを明記する。
`TBD` の多用で薄くしない。

