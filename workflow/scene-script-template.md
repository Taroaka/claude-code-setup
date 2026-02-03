# Scene Script (Q&A) (DRAFT)

```yaml
scene_script_metadata:
  topic: "<topic>"
  scene_id: <scene_id>
  target_seconds: 30
  question: "<question>"

# Narration structure (30–60s)
narration:
  hook: "<ask the question>"
  answer: "<one-sentence answer>"
  evidence:
    - "<evidence point 1>"
    - "<evidence point 2>"
    - "<evidence point 3>"
  close: "<optional: recap or next question>"

text_overlay:
  main_text: "<main_text>"
  sub_text: "<question>"

notes:
  - "Visual style (real/abstract) is deferred; keep prompts flexible."
```

