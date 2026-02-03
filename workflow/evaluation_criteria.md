# Evaluation Criteria (Prompt Optimizer)

本ファイルは、`workflow/datasets/` の dataset（入力例 + 理想出力）に対して、
「生成プロンプト（または生成指示）がどの程度うまく作れているか」を評価するための基準を定義する。

目的:
- scene spec（`script.md` の scene）→ image/video/overlay 等の生成指示を **安定して作れる**ようにする
- “良し悪し”を人の感覚で終わらせず、差分分析→改善の反復ができるようにする

## 対象（何を評価するか）

最小の対象は次のいずれか:
- Scene → `image_prompt`（静止画生成用）
- Scene → `motion_prompt`（image-to-video 用）
- Scene → `text_overlay`（テロップ内容/タイミング）

拡張:
- negative prompt
- seed / style params（provider依存のため、まずは任意）

## スコアリング（例）

重みは固定しない。まずは 0–100 の主観採点で運用し、後で調整する。

### 1) Scene Alignment（整合性）

- scene の意図（場所/時間/状況/感情/行動）と、生成指示が一致している
- narration と絵が矛盾しない

### 2) Character Consistency（キャラクター一貫性）

- character bible / fixed prompts に沿う
- 服装・髪・年齢感がブレない

### 3) Cinematic Quality（映像指示の質）

- shot（画角/アングル/構図/照明）が具体
- “何をどう見せるか”が明確で、生成に必要十分

### 4) Provider Robustness（プロバイダ差分耐性）

- 特定ベンダ依存の言い回しを避け、一般的な記述で成立している
- provider 固有機能（参照強度等）は別フィールドで切れる

### 5) Overlay Readability（テロップ可読性）

- 短く、読みやすい（視線誘導ができる）
- 字幕/テロップと映像が衝突しにくい（背景/位置/長さの配慮）

### 6) Safety / Compliance（必要なら）

- 明確に禁止したい要素が入っていない（ブランド/著作物/人物など）

## 出力（評価ログの書き方）

各イテレーションで最低限これを残す:

```yaml
iteration: 1
sampled_datasets:
  - "workflow/datasets/momotaro_v1.yaml"
samples_used:
  - case_id: "momotaro_scene1"
    score:
      scene_alignment: 80
      character_consistency: 60
      cinematic_quality: 70
      provider_robustness: 75
      overlay_readability: 85
    issues:
      - "主題は合っているが、時間帯が曖昧"
    fixes:
      - "prompt に time_of_day を明示"
stop_condition_met: false
```

停止条件（例）:
- 最大 N イテレーション
- 平均スコア >= 90

