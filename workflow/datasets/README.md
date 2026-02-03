# Datasets for Prompt Optimizer

`workflow/datasets/` は、Prompt Optimizer 用の dataset を置く場所。

## 目的

- 入力（scene spec）に対して、理想の出力（prompt / 指示）をペアで持つ
- 過適合を避けるため、複数 dataset を用意し、サンプリングして評価する

## 形式（暫定）

- `.yaml` を推奨
- 1ファイルに複数 case を入れて良い

### 最小スキーマ（例）

```yaml
dataset_metadata:
  id: "momotaro_v1"
  topic: "桃太郎"
  created_at: "2026-01-24T00:00:00+09:00"

cases:
  - case_id: "momotaro_scene1"
    input:
      scene:
        scene_id: 1
        narration_text: "..."
        visual_description: "..."
    ideal_output:
      image_prompt: "..."
      motion_prompt: "..."
      overlay:
        main_text: "..."
        sub_text: "..."
```

