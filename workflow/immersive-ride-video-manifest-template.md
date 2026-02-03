# Immersive Ride Video Manifest Template (run root)

This template is used for `output/<topic>_<timestamp>/video_manifest.md` in `/toc-immersive-ride`.

```yaml
video_metadata:
  topic: "<topic>"
  source_story: "output/<topic>_<timestamp>/story.md"
  created_at: "<ISO8601>"
  duration_seconds: 0   # filled after narration is generated (optional)
  aspect_ratio: "16:9"
  resolution: "1280x720"
  frame_rate: 24

assets:
  character_bible:
    - character_id: "guide_character"
      reference_images:
        - "assets/characters/guide_character.png"
      fixed_prompts:
        - "photorealistic, cinematic, practical effects, 8K quality, ultra detailed textures"
        - "First-person POV from ride action boat"
        - "Realistic hands gripping ornate brass safety bar"
      notes: "Generate this character image first and reuse as reference in every scene image."

  style_guide:
    visual_style: "photorealistic, cinematic, practical effects"
    forbidden:
      - "animated"
      - "animation"
      - "cartoon"
      - "anime"
      - "illustrated"
      - "drawing"
    reference_images: []

scenes:
  # 0) Character image (optional as part of scenes, or generated separately)
  - scene_id: 0
    timestamp: "00:00-00:08"
    image_generation:
      tool: "google_nanobanana_pro"
      prompt: |
        Photorealistic cinematic portrait of the guide character for the ride story.
        No text in image. Realistic lighting, practical effects feel.
      output: "assets/characters/guide_character.png"
      aspect_ratio: "16:9"
      image_size: "2K"
      references: []
      iterations: 4
      selected: null

  # 1) Scene still images + transitions
  - scene_id: 1
    timestamp: "00:00-00:08"
    image_generation:
      tool: "google_nanobanana_pro"
      prompt: |
        First-person POV from ride action boat, photorealistic cinematic, practical effects.
        Realistic hands gripping ornate brass safety bar in the foreground.
        The boat travels on a theme park track (central rail visible), entering the world of <topic>.
        The guide character appears ahead. Seamless continuity setup for next scene.
        No text in image. Avoid anime/cartoon/illustration.
      output: "assets/scenes/scene1.png"
      aspect_ratio: "16:9"
      image_size: "2K"
      references: ["assets/characters/guide_character.png"]
      iterations: 4
      selected: null
    video_generation:
      tool: "google_veo_3_1"
      duration_seconds: 8
      first_frame: "assets/scenes/scene1.png"
      last_frame: "assets/scenes/scene2.png"
      motion_prompt: "Ride action boat moves forward smoothly along the track; natural lighting transition."
      output: "assets/scenes/scene1_to_2.mp4"
    audio:
      narration:
        text: "TODO: full narration text"
        tool: "elevenlabs"
        output: "assets/audio/narration.mp3"
        normalize_to_scene_duration: false

  - scene_id: 2
    timestamp: "00:08-00:16"
    image_generation:
      tool: "google_nanobanana_pro"
      prompt: |
        First-person POV from ride action boat, photorealistic cinematic, practical effects.
        Realistic hands gripping ornate brass safety bar in the foreground.
        The guide character appears, pointing to the next event in <topic> world.
        Track continues; set up seamless transition to next scene.
        No text in image. Avoid anime/cartoon/illustration.
      output: "assets/scenes/scene2.png"
      aspect_ratio: "16:9"
      image_size: "2K"
      references: ["assets/characters/guide_character.png"]
      iterations: 4
      selected: null
    video_generation:
      tool: "google_veo_3_1"
      duration_seconds: 8
      first_frame: "assets/scenes/scene2.png"
      last_frame: "assets/scenes/scene3.png"
      motion_prompt: "Continue forward along the track with a gentle curve; maintain POV and hands."
      output: "assets/scenes/scene2_to_3.mp4"

  - scene_id: 3
    timestamp: "00:16-00:24"
    image_generation:
      tool: "google_nanobanana_pro"
      prompt: |
        First-person POV from ride action boat, photorealistic cinematic, practical effects.
        Realistic hands gripping ornate brass safety bar in the foreground.
        A climactic reveal in the world of <topic>, with the guide character clearly present.
        The boat remains aligned to the central track; lighting transitions naturally from the previous scene.
        No text in image. Avoid anime/cartoon/illustration.
      output: "assets/scenes/scene3.png"
      aspect_ratio: "16:9"
      image_size: "2K"
      references: ["assets/characters/guide_character.png"]
      iterations: 4
      selected: null
```
