# Tasklist: Creative Selection Policy (創造と選択)

## 1. ドキュメント更新

- [ ] `docs/story-creation.md` に「創造と選択」「ハイブリッド承認ゲート」を追加し、Hero's Journey を参考枠へ移す
- [ ] `docs/information-gathering.md` の Hero's Journey 前提の記述を「参考」へ弱める
- [ ] `docs/script-creation.md` で「Hero's Journey への当てはめ」を目的にしない旨を追記（必要最小）

## 2. テンプレ更新

- [ ] `workflow/research-template.yaml` / `workflow/research-template.production.yaml` に conflicts / selection cues を追加（既存キーは残す）
- [ ] `workflow/story-template.yaml` に optional な selection/hybridization セクションを追加

## 3. エージェント更新

- [ ] `.claude/agents/deep-researcher.md` に conflicts / selection / hybrid proposal の出力を追記
- [ ] `.claude/agents/director.md` に「複数案→選択→必要なら承認」を追記し、Hero's Journey 固定を外す
- [ ] `.claude/agents/scene-scriptwriter.md` / `.claude/agents/immersive-scriptwriter.md` に「新規ハイブリッドは承認必須」を追記

## 4. コマンド説明更新

- [ ] `.claude/commands/toc/toc-run.md` と `.claude/commands/toc/toc-scene-series.md` に「創造と選択」の位置づけを短く追記
- [ ] `.claude/commands/toc/toc-immersive-ride.md` に「ハイブリッド承認」の注意を追記

## 5. 整合チェック

- [ ] `rg` で “英雄の旅が必須/失格” のような文言が残っていないか確認
- [ ] `python -m compileall .`（可能なら）でドキュメント更新が実行に影響しないことを確認

