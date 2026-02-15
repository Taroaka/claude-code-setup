# Requirements: Folktale research agent (Codex skill)

## Background

日本の物語（例: 桃太郎 / 浦島太郎）をベースに動画生成を進めているが、他国の民話・神話・伝承については網羅的な知識がない。
「この国（地域）の物語を調べて、制作に使えるネタと骨格を出してほしい」を **再現性ある手順**としてCodexに持たせたい。

## Goals

- 国/地域を指定すると、その文化圏の代表的な民話・神話を **候補リスト**として提示できる
- 候補から1本選んだら、ToCの調査テンプレ（`workflow/research-template.yaml`）に沿って **Story-first** で骨格を出力できる
- 出力には「どの情報をどのsceneで使うか」を意識して、後続の story/script/manifest に接続しやすい形にする

## Non-goals

- 自動でWebにアクセスして収集・スクレイピングする実装（このスコープではやらない）
- 著作権/パブリックドメイン判定の最終判断（注意喚起と確認項目は出すが、法的確定はしない）

## Constraints / Quality bar

- 「裏話・小ネタ」より先に、必ず canonical synopsis / beat sheet / 登場人物最小セットを確定する（`docs/information-gathering.md` に準拠）
- 既知知識だけで断定しない。曖昧な点は「未検証」として明示し、必要な検証観点を出す
- スキルは `codex_skills/` に置き、`scripts/ai/install-codex-skills.sh` で `~/.codex/skills/` に同期できること

## User stories

- US1: 「ギリシャの物語のネタを出して」→ 代表的な神話/叙事詩/英雄譚の候補が10本程度、1行要約＋推し理由付きで出る
- US2: 「その中からオルフェウスをベースにToC用の調査yamlを作って」→ `workflow/research-template.yaml` を満たす骨格が出る
- US3: 「子ども向け/怖すぎない/没入型ライド向き」など制約を反映できる

