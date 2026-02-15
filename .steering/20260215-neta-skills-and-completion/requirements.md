# Requirements: Neta collection skills + completion tracking + vertical shorts

## Background

ToC の制作では「ネタ収集 → 調査 → story/script → manifest → 素材生成 → 結合 → 人間レビュー → 完成」が反復になる。
日本の民話（桃太郎/浦島太郎）以外にも、以下の “ネタ種別” を増やしていきたい。

- その1: 各国の物語（既存: `folktale-researcher`）
- その2: 世界で話題の自己啓発系人物（億万長者/ポッドキャスト等）を紹介できる
- その3: AI が考えたオリジナル◯◯（世界観/物語/コンセプト）
- その4: 時代解説（例: 縄文時代）

さらに、各 `output/<topic>_<timestamp>/` について「最終結合 video.mp4 ができたか」「人間が完成OKを出したか」を
**state.txt を一次ソース**として追記管理したい。
完成した run のみを入力にして、横動画（16:9）から縦ショート（9:16, ~60s）を作れるようにしたい。

## Goals

### G1: ネタ収集 skills の追加（Codex）

- その2〜その4のスキルを `codex_skills/` に追加する
- 入口としてカテゴリ選択を促す “メタ” スキルも用意する（Separate + Meta）

### G2: 完成判断の記録（state.txt only）

- `workflow/state-schema.txt` に “render結果 + 人間承認” のキーを追加
- `scripts/toc-state.py` で state の作成/追記/承認/表示を自動化する
- `scripts/toc-immersive-ride-generate.sh` を実行すると、state.txt に render 成否が追記される

### G3: 縦ショート生成（completionが整ったrunのみ）

- `review.video.status=approved` の run のみを入力に、縦ショート mp4 を生成する
- 変換は「既存の横動画（16:9）を中心cropで9:16に」する（新規生成なし）
- 成功したら state.txt に short の成果物パスを追記する

## Non-goals

- 自動Webスクレイピング/恒常的クロール（“Hybrid”として、使える環境では検索、使えない環境ではユーザーにソース貼り付けを依頼）
- 収益/投資助言、個人の私的情報の収集
- 縦ショートの新規AI生成（今回は crop/pad ではなく crop のみ実装）

## Constraints

- `state.txt` は `output/<topic>_<timestamp>/state.txt` の追記型（`---` 区切り）を維持する
- “完成”は **人間が明示的に approved を付ける**ことを必須にする（render 成功=完成ではない）
- テストは `pytest` 前提にせず、既存の `python scripts/run_unit_tests.py`（unittest）で回す

## Success criteria (acceptance)

- A1: `scripts/toc-state.py show --run-dir output/浦島太郎_20260208_1515_immersive` で現在状態が表示できる
- A2: `scripts/toc-immersive-ride-generate.sh --run-dir output/<topic>_<timestamp>` が state に `runtime.render.status` と `artifact.video` を追記する
- A3: 未承認の run に対して `scripts/make-vertical-short.py` は中断し、承認方法を案内する
- A4: 承認済み run で縦ショートを生成し、state に `artifact.video.short.01` と `runtime.stage=shorts` を追記できる

