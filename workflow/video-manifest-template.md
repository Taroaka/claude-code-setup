# 動画マニフェスト: テンプレート

`docs/video-generation.md` の出力スキーマに準拠した作業テンプレートです。

- 出力先: `output/videos/<topic>_<timestamp>_manifest.md`
  - 1物語1フォルダ運用の場合: `output/<topic>_<timestamp>/video_manifest.md`
- 目的: 生成素材・選定・合成の管理

```yaml
# === メタ情報 ===
video_metadata:
  topic: "<topic>"
  source_story: "output/<topic>_<timestamp>/story.md"
  created_at: "<ISO8601>"
  duration_seconds: 60
  aspect_ratio: "9:16"
  resolution: "1080x1920"

# === 素材管理 ===
assets:
  character_bible:
    - character_id: "protagonist"
      reference_images:
        - "assets/characters/protagonist_front.png"
        - "assets/characters/protagonist_side.png"
      fixed_prompts:
        - "short black hair"
        - "traditional japanese attire"

  style_guide:
    visual_style: "cinematic, warm tones"
    reference_images:
      - "assets/styles/reference_1.png"

# === シーン別素材 ===
scenes:
  - scene_id: 1
    timestamp: "00:00-00:10"
    image_generation:
      tool: "dalle3"
      prompt: "quiet rural village at dawn"
      output: "assets/scenes/scene1_base.png"
      iterations: 4
      selected: 1
    video_generation:
      tool: "runway"
      input_image: "assets/scenes/scene1_base.png"
      motion_prompt: "slow pan"
      output: "assets/scenes/scene1_video.mp4"
    audio:
      narration:
        text: "昔、ある村に桃から生まれた少年がいました。"
        tool: "openai_tts"
        output: "assets/audio/scene1_narration.mp3"
      bgm:
        source: "assets/audio/bgm_intro.mp3"
        volume: 0.3
      sfx: []

# === 最終出力 ===
final_output:
  video_file: "output/<topic>_<timestamp>/video.mp4"
  thumbnail: "output/<topic>_<timestamp>/thumb.png"

# === 品質チェック ===
quality_check:
  visual_consistency: false
  audio_sync: false
  subtitle_readable: false
  aspect_ratio_correct: true
```

---

## 参考コマンド（結合/レンダリング）

`scripts/render-video.sh` を利用する場合の例:

```bash
scripts/render-video.sh \
  --clip-list clips.txt \
  --narration narration.mp3 \
  --bgm bgm.mp3 \
  --srt subtitles.srt \
  --out output/<topic>_<timestamp>/video.mp4
```
