# Immersive Cloud Island Walk Video Manifest Template (run root)

This template is used for `output/<topic>_<timestamp>/video_manifest.md` in `/toc-immersive-ride` when using the `cloud_island_walk` experience.

```yaml
video_metadata:
  topic: "<topic>"
  source_story: "output/<topic>_<timestamp>/story.md"
  created_at: "<ISO8601>"
  duration_seconds: 0   # filled after narration is generated (optional)
  experience: "cloud_island_walk"
  aspect_ratio: "16:9"
  resolution: "1280x720"
  frame_rate: 24

assets:
  character_bible: []

  style_guide:
    visual_style: "photorealistic, cinematic, practical effects"
    forbidden:
      - "animated"
      - "animation"
      - "cartoon"
      - "anime"
      - "illustrated"
      - "drawing"
      - "third-person"
      - "third-person view"
      - "over-the-shoulder"
      - "selfie"
      - "camera facing the subject"
      - "on-screen text"
      - "subtitle text"
      - "watermark"
      - "logo"
    reference_images: []

  # Object / setpiece bible (optional but recommended for film-quality detail).
  # In cloud_island_walk, most philosophical concepts should be embodied as physical setpieces/artifacts.
  object_bible: []
  # - object_id: "tbd_metaphor_gate"
  #   kind: "setpiece"
  #   reference_images:
  #     - "assets/objects/tbd_metaphor_gate.png"
  #   fixed_prompts:
  #     - "Real-world materials + construction; no sci-fi HUD; no text signage"
  #     - "Readable metaphor via shape/light/motion, not labels"
  #   cinematic:
  #     role: "What role does this play in the film (threshold/temptation/revelation)?"
  #     visual_takeaways:
  #       - "What should the audience understand purely from the visuals?"
  #     spectacle_details:
  #       - "Non-plot visual wonders that make it exciting (moving parts, hidden rooms, shows)"
  #   notes: null

scenes:
  # Scene still images + transitions (guide is narration-only)
  #
  # Zones (recommended planning):
  # - Zones: 4–10 (minimum is 起承転結 = 4)
  # - Scenes per zone: 3–10
  #
  # scene_id scheme (recommended):
  # - Zone 1: 110,120,130...
  # - Zone 2: 210,220,230...
  # - Zone 3: 310,320,330...
  # - Zone 4: 410,420,430...
  #
  # Notes:
  # - No on-screen text. Convey everything via imagery/metaphor.
  # - Hands/anchor props are NOT required; keep POV stable via framing (path centered, horizon stable, consistent camera height).
  - scene_id: 10
    timestamp: "00:00-00:08"
    image_generation:
      tool: "google_nanobanana_pro"
      character_ids: []
      object_ids: []
      prompt: |
        [GLOBAL / INVARIANTS]
        First-person POV walking forward. Stable horizon, consistent camera height, natural gait.
        Path / leading lines centered to enforce forward motion continuity.
        Paradise island floating above a sea of clouds (practical set-piece feel; no sci-fi HUD).
        Photorealistic, cinematic, practical effects. Natural film lighting.
        No text, no subtitles, no watermark, no logo.

        [PROPS / SETPIECES]

        [SCENE]
        Arrival: you emerge from soft clouds onto a floating stone path that leads to a luminous island gate.
        Key moment: the island’s first landmark hints at the core philosophical question of <topic> (show it as a physical metaphor, not text).
        Composition: path centered; gate mid-ground; cloud ocean far background; foreground contains practical set textures (stone, moss, mist).

        [CONTINUITY]
        Set up next: the path continues inward; lighting warms slightly; keep the same forward direction and camera height.

        [AVOID]
        animated, cartoon, anime, illustrated, drawing. Distorted hands, extra fingers. Any text.
      output: "assets/scenes/scene10.png"
      aspect_ratio: "16:9"
      image_size: "2K"
      references: []
      iterations: 4
      selected: null
    video_generation:
      tool: "google_veo_3_1"
      duration_seconds: 8
      first_frame: "assets/scenes/scene10.png"
      last_frame: "assets/scenes/scene20.png"
      motion_prompt: "Walk forward smoothly along the floating stone path; subtle cloud drift; maintain POV and hands with compass."
      output: "assets/scenes/scene10_to_20.mp4"
    audio:
      narration:
        text: "TODO: full narration text"
        tool: "elevenlabs"
        output: "assets/audio/narration.mp3"
        normalize_to_scene_duration: false

  - scene_id: 20
    timestamp: "00:08-00:16"
    image_generation:
      tool: "google_nanobanana_pro"
      character_ids: []
      object_ids: []
      prompt: |
        [GLOBAL / INVARIANTS]
        First-person POV walking forward. Stable horizon, consistent camera height, natural gait.
        Path / leading lines centered. Paradise island floating above clouds.
        Photorealistic, cinematic, practical effects.
        No text, no subtitles, no watermark, no logo.

        [PROPS / SETPIECES]

        [SCENE]
        Zone 1: the “foundation” area of the island (a garden / library / temple) that embodies the first key idea of <topic>.
        Key moment: you approach a tangible metaphor object (e.g., mirrors, weights, bridges, knots) that makes the idea intuitive without words.
        Composition: metaphor object mid-ground; deeper island path background; path remains centered.

        [CONTINUITY]
        Must match previous: same forward motion; same camera height; consistent lighting direction.
        Set up next: a gentle curve in the path leads toward a more complex “paradox” zone.

        [AVOID]
        animated, cartoon, anime, illustrated, drawing. Distorted hands, extra fingers. Any text.
      output: "assets/scenes/scene20.png"
      aspect_ratio: "16:9"
      image_size: "2K"
      references: []
      iterations: 4
      selected: null
    video_generation:
      tool: "google_veo_3_1"
      duration_seconds: 8
      first_frame: "assets/scenes/scene20.png"
      last_frame: "assets/scenes/scene30.png"
      motion_prompt: "Continue walking forward; subtle parallax; keep hands/compass stable; clouds drift gently below."
      output: "assets/scenes/scene20_to_30.mp4"

  - scene_id: 30
    timestamp: "00:16-00:24"
    image_generation:
      tool: "google_nanobanana_pro"
      character_ids: []
      object_ids: []
      prompt: |
        [GLOBAL / INVARIANTS]
        First-person POV walking forward. Stable horizon, consistent camera height, natural gait.
        Path / leading lines centered. Paradise island floating above clouds.
        Photorealistic, cinematic, practical effects.
        No text, no subtitles, no watermark, no logo.

        [PROPS / SETPIECES]

        [SCENE]
        Zone 2: the “paradox / tension” area of the island, where two ideas collide as physical architecture (bridges crossing, stairs looping, water flowing upward).
        Key moment: the metaphor becomes more visually complex, hinting at the deeper philosophical conflict in <topic>.
        Composition: paradox structure mid-ground; a calm summit destination far background; path remains centered.

        [CONTINUITY]
        Must match previous: same POV and forward direction; consistent camera height.
        Set up next: reveal a clear “synthesis” path toward the summit.

        [AVOID]
        animated, cartoon, anime, illustrated, drawing. Distorted hands, extra fingers. Any text.
      output: "assets/scenes/scene30.png"
      aspect_ratio: "16:9"
      image_size: "2K"
      references: []
      iterations: 4
      selected: null
```
