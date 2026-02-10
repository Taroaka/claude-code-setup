# Script Method: Philosophical Cloud-Island Walkthrough

## Use when
- 「哲学的な思考を要する内容」を AI 動画で解説したい
- 物語の“出来事”よりも、概念理解の“深化”を体験として見せたい
- `/toc-immersive-ride --experience cloud_island_walk` の台本/manifest を作るとき

## Core idea
「調査で得た構造（論点/前提/反論/統合/含意）」を、雲上の島の“ゾーン”として実写の比喩で具現化する。
視聴者は島に到着し、歩みを進めるほど理解が深まる（＝シーン進行＝理解の進行）。

## Scene structure (recommended)
1) **Arrival / Hook**: 島の入口（問いの門）で主問題を提示（文字ではなく象徴物で）
2) **Foundation Zone**: 前提/定義/直感を、庭園・図書館・器具などの物理メタファで見せる
3) **Tension Zone**: 反例/パラドックス/対立を、交差する橋・ループする階段などで視覚化
4) **Synthesis Zone**: 観点の切替/統合/条件付き結論を、“頂上”や“光が差す道”として表現
5) **Return / Takeaway**: 島を俯瞰し、限界と持ち帰る指針（次に考える問い）を提示

## Visual constraints (non-negotiable)
- First-person POV を固定（歩く方向のブレを抑える）
- 手元アンカーは必須ではない（手が映らなくてもよい）
- 代わりに「連続性のアンカー」を固定する（例: path/leading lines を常にセンター、地平線の安定、一定のカメラ高さ）
- “概念の説明”を **看板の文字**でやらない（No on-screen text）
- 道/橋/階段など「前進の導線」を必ず画面に入れる（scene間の連続性）
- 禁止: third-person / over-the-shoulder / selfie（外側カメラに切り替わる指示）

## Manifest tips
- `video_metadata.experience: "cloud_island_walk"` を必ず入れる
- Zones は 4–10（最低 4 = 起承転結）、Zones 内の scenes は 3–10 を目安に設計する
- scene_id は「ゾーンが分かる」規則を推奨（例: Zone1=110,120..., Zone2=210,220...）
- キャラクターがいないsceneでも `image_generation.character_ids: []` を明示する

## Quality gate
- 各sceneが「1つの理解の前進」を担っている（重複しない）
- 反論/例外/限界が1回は登場し、安易に断言しない
- 結論は“思考の道具”として提示される（行動指針 or 次の問い）
