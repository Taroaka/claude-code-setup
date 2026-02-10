# Scene Video Manifest Template (single scene)

This template is used for `output/<topic>_<timestamp>/scenes/sceneXX/video_manifest.md`.

```yaml
video_metadata:
  topic: "<topic>"
  source_run: "output/<topic>_<timestamp>/"
  source_scene_script: "output/<topic>_<timestamp>/scenes/sceneXX/script.md"
  created_at: "<ISO8601>"
  duration_seconds: 30
  aspect_ratio: "9:16"
  resolution: "1080x1920"

assets:
  style_guide:
    visual_style: "tbd"
    reference_images: []

scenes:
  - scene_id: 1
    timestamp: "00:00-00:30"
    image_generation:
      # tool: "google_nanobanana_pro"
      # tool: "seadream"        # Seedream 4.5 (OpenAI Images compatible; see SEADREAM_* env)
      tool: "google_nanobanana_pro"
      character_ids: ["character_id_here"]  # Use [] for B-roll scenes with no characters visible
      prompt: |
        [GLOBAL / INVARIANTS]
        TODO: style/pov invariants. No text, no subtitles, no watermark.

        [CHARACTERS]
        TODO: who is present + must-match reference rules (if any).

        [SCENE]
        TODO: setting + key moment + composition (foreground/midground/background).

        [CONTINUITY]
        TODO: must match prev / set up next.

        [AVOID]
        TODO: forbid list (e.g., text/watermark/logo + unwanted styles).
      output: "assets/scenes/scene1_base.png"
      iterations: 4
      selected: null
    video_generation:
      # tool: "google_veo_3_1"
      # tool: "kling_3_0"
      tool: "google_veo_3_1"
      input_image: "assets/scenes/scene1_base.png"
      motion_prompt: "TODO: camera/motion"
      output: "assets/scenes/scene1_video.mp4"
    audio:
      narration:
        text: "TODO: narration"
        tool: "elevenlabs"
        output: "assets/audio/scene1_narration.mp3"
      bgm:
        source: null
        volume: 0.0
      sfx: []
    text_overlay:
      main_text: "<main_text>"
      sub_text: "<question>"

final_output:
  video_file: "video.mp4"
  thumbnail: "thumb.png"

quality_check:
  visual_consistency: false
  audio_sync: false
  subtitle_readable: false
  aspect_ratio_correct: true
```
