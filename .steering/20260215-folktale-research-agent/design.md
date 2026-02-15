# Design: Folktale research agent (Codex skill)

## Approach

Codex CLI の **skill** として「国別・文化圏別の物語ネタ調査」を定義する。
実装コードではなく、プロンプト運用（手順・判断基準・出力フォーマット）を SKILL.md に封入する。

## Skill I/O

### Inputs (prompt)

- 国/地域（例: "Ireland", "West Africa", "Andes"）
- 望むトーン/対象年齢/NG（例: 児童向け、残酷描写NG、宗教への配慮）
- 目的（ネタ出しのみ / 1本深掘りして research yaml 生成）

### Outputs

1) **Idea slate（ネタ候補）**
   - 8〜12本程度
   - 各候補: 1行要約 / 主要モチーフ / 映像化の推しポイント / 注意点（センシティブ/権利/地域差）

2) **Deep dive（1本選択時）**
   - `workflow/research-template.yaml` に沿った Story-first 出力
   - scene_plan は 1..20 の骨格を最低限埋める（後段で伸ばせる）
   - sources_used は「確認すべき典拠」を列挙（Webアクセスできない場合も、典拠候補名を出す）

## Verification policy

- モデル内知識で“だいたいの骨”は出せるが、固有名詞・地域差・成立/典拠などは誤り得るため、
  「未検証」マークと検証TODOを必ず付ける。
- Webが使える環境では、最低限 Wikipedia / 学術系/博物館/図書館等の一次/準一次に当たる方針を推奨。

## Repo placement

- Codex skill の正本: `codex_skills/folktale-researcher/SKILL.md`
- インストール: `scripts/ai/install-codex-skills.sh`（既存フローに乗せる）
- 使い方の追記: `docs/implementation/assistant-tooling.md`（Codex skill 一覧として最小追記）

