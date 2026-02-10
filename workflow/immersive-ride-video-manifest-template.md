# Immersive Ride Video Manifest Template (run root)

This template is used for `output/<topic>_<timestamp>/video_manifest.md` in `/toc-immersive-ride`.

```yaml
video_metadata:
  topic: "<topic>"
  source_story: "output/<topic>_<timestamp>/story.md"
  created_at: "<ISO8601>"
  duration_seconds: 0   # filled after narration is generated (optional)
  experience: "ride_action_boat"
  aspect_ratio: "16:9"
  resolution: "1280x720"
  frame_rate: 24

assets:
  character_bible:
    # Story characters (examples). The guide is narration-only (no visual guide character).
    - character_id: "protagonist"
      reference_images:
        - "assets/characters/protagonist_front.png"
      fixed_prompts:
        - "protagonist matches the reference image exactly (same face, hair, outfit)"
      notes: "Generate a clean full-body turnaround reference first, then reuse as reference in scenes where this character appears."

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

  # Object / setpiece bible (optional but recommended for film-quality detail).
  # Treat key items/places like "characters": design them once, generate reference images, then reference them in scenes.
  object_bible: []
  # - object_id: "tbd_setpiece"
  #   kind: "setpiece"  # setpiece|artifact|phenomenon
  #   reference_images:
  #     - "assets/objects/tbd_setpiece.png"
  #   fixed_prompts:
  #     - "Material + construction details that must stay consistent"
  #     - "Mechanism / showmanship / temptation design cues"
  #     - "No engraved text, no signage; convey meaning via form/light/motion"
  #   cinematic:
  #     role: "What role does this play in the film (plot/emotion/theme)?"
  #     visual_takeaways:
  #       - "What should the audience understand purely from the visuals?"
  #     spectacle_details:
  #       - "Non-plot visual wonders that make it exciting (shows, hidden rooms, moving parts)"
  #   notes: null

scenes:
  # 0) Character reference (recommended)
  # When you run `scripts/toc-immersive-ride-generate.sh`, it will auto-generate side/back views and a combined strip
  # from this front output (so you don't have to hand-author 3 prompts).
  - scene_id: 0
    image_generation:
      tool: "google_nanobanana_pro"
      character_ids: ["protagonist"]
      object_ids: []
      prompt: |
        [GLOBAL / INVARIANTS]
        Photorealistic, cinematic, practical effects. Natural film lighting.
        No text, no subtitles, no watermark, no logo.

        [SCENE]
        Character turnaround reference for the protagonist.
        Full-body head-to-toe, feet fully visible (no cropping). Neutral relaxed pose, centered framing.
        Clean neutral background.

        [AVOID]
        animated, cartoon, anime, illustrated, drawing. Any text.
      output: "assets/characters/protagonist_front.png"
      aspect_ratio: "16:9"
      image_size: "2K"
      references: []
      iterations: 4
      selected: null

  # 1) Scene still images + transitions (guide is narration-only)
  # Recommended: use scene_id in steps of 10 so you can insert mid-scenes later (e.g., 35 between 30 and 40).
  - scene_id: 10
    timestamp: "00:00-00:08"
    image_generation:
      tool: "google_nanobanana_pro"
      character_ids: ["protagonist"]
      object_ids: []
      prompt: |
        [GLOBAL / INVARIANTS]
        First-person POV from ride action boat. Realistic hands gripping ornate brass safety bar in the lower foreground.
        Theme park ride track with central rail visible, centered. Photorealistic, cinematic, practical effects.
        No text, no subtitles, no watermark, no logo.

        [CHARACTERS]
        The story character(s) must match their reference image exactly (same face, hair, outfit).

        [PROPS / SETPIECES]

        [SCENE]
        Setting: the ride enters the world of <topic>. Practical set pieces, real lighting.
        Key moment: the first story character appears ahead, drawing you into the world.
        Composition: hands+bar foreground; track centered; story character mid-ground; destination far background.

        [CONTINUITY]
        Set up next: track continues smoothly; lighting transitions naturally into scene 2.

        [AVOID]
        animated, cartoon, anime, illustrated, drawing. Distorted hands, extra fingers. Any text.
      output: "assets/scenes/scene10.png"
      aspect_ratio: "16:9"
      image_size: "2K"
      references: []
      iterations: 4
      selected: null
    video_generation:
      # tool: "google_veo_3_1"
      # tool: "kling_3_0"
      tool: "google_veo_3_1"
      duration_seconds: 8
      first_frame: "assets/scenes/scene10.png"
      last_frame: "assets/scenes/scene20.png"
      motion_prompt: "Ride action boat moves forward smoothly along the track; natural lighting transition."
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
      character_ids: ["protagonist"]
      object_ids: []
      prompt: |
        [GLOBAL / INVARIANTS]
        First-person POV from ride action boat. Realistic hands gripping ornate brass safety bar in the lower foreground.
        Theme park ride track with central rail visible, centered. Photorealistic, cinematic, practical effects.
        No text, no subtitles, no watermark, no logo.

        [CHARACTERS]
        The story character(s) must match their reference image exactly.

        [PROPS / SETPIECES]

        [SCENE]
        Setting: the ride advances deeper into the <topic> world; practical fog and subtle water spray.
        Key moment: the story character reacts to the next event ahead.
        Composition: story character mid-ground; event/reveal far background; track remains centered.

        [CONTINUITY]
        Must match previous: same hands + brass bar details; same forward direction.
        Set up next: gentle left curve begins; cue the next scene reveal.

        [AVOID]
        animated, cartoon, anime, illustrated, drawing. Distorted hands, extra fingers. Any text.
      output: "assets/scenes/scene20.png"
      aspect_ratio: "16:9"
      image_size: "2K"
      references: []
      iterations: 4
      selected: null
    video_generation:
      # tool: "google_veo_3_1"
      # tool: "kling_3_0"
      tool: "google_veo_3_1"
      duration_seconds: 8
      first_frame: "assets/scenes/scene20.png"
      last_frame: "assets/scenes/scene30.png"
      motion_prompt: "Continue forward along the track with a gentle curve; maintain POV and hands."
      output: "assets/scenes/scene20_to_30.mp4"

  - scene_id: 30
    timestamp: "00:16-00:24"
    image_generation:
      tool: "google_nanobanana_pro"
      character_ids: ["protagonist"]
      object_ids: []
      prompt: |
        [GLOBAL / INVARIANTS]
        First-person POV from ride action boat. Realistic hands gripping ornate brass safety bar in the lower foreground.
        Theme park ride track with central rail visible, centered. Photorealistic, cinematic, practical effects.
        No text, no subtitles, no watermark, no logo.

        [CHARACTERS]
        The story character(s) must match their reference image exactly and is clearly visible.

        [PROPS / SETPIECES]

        [SCENE]
        Setting: a climactic reveal area in the <topic> world, built as practical set pieces with cinematic lighting.
        Key moment: the reveal fills the background while the story character reacts to it.
        Composition: hands+bar foreground; story character mid-ground; reveal far background; track centered.

        [CONTINUITY]
        Must match previous: same lighting direction and forward motion setup.

        [AVOID]
        animated, cartoon, anime, illustrated, drawing. Distorted hands, extra fingers. Any text.
      output: "assets/scenes/scene30.png"
      aspect_ratio: "16:9"
      image_size: "2K"
      references: []
      iterations: 4
      selected: null

  # Example B-roll (no story character visible; still must keep POV invariants)
  - scene_id: 40
    timestamp: "00:24-00:32"
    image_generation:
      tool: "google_nanobanana_pro"
      character_ids: []
      object_ids: []
      prompt: |
        [GLOBAL / INVARIANTS]
        First-person POV from ride action boat. Realistic hands gripping ornate brass safety bar in the lower foreground.
        Theme park ride track with central rail visible, centered. Photorealistic, cinematic, practical effects.
        No text, no subtitles, no watermark, no logo.

        [PROPS / SETPIECES]

        [SCENE]
        B-roll: environment-only moment in the <topic> world (no story characters visible). Practical set pieces, cinematic lighting.

        [AVOID]
        animated, cartoon, anime, illustrated, drawing. Any text.
      output: "assets/scenes/scene40.png"
      aspect_ratio: "16:9"
      image_size: "2K"
      references: []
      iterations: 4
      selected: null
```
