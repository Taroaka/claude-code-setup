#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

try:
    import yaml  # type: ignore[import-not-found]
except ModuleNotFoundError:  # pragma: no cover
    yaml = None


def extract_yaml_block(text: str) -> str:
    match = re.search(r"```yaml\s*\n(.*?)\n```", text, flags=re.DOTALL)
    if not match:
        raise SystemExit("No ```yaml ... ``` block found.")
    return match.group(1)


def load_story_scene_map(story_path: Path) -> dict[int, dict]:
    if not story_path.exists() or yaml is None:
        return {}
    text = story_path.read_text(encoding="utf-8")
    blocks = re.findall(r"```yaml\s*\n(.*?)\n```", text, flags=re.DOTALL)
    if not blocks:
        return {}
    data = yaml.safe_load(blocks[-1])
    scenes = (((data or {}).get("script") or {}).get("scenes") or [])
    result: dict[int, dict] = {}
    for scene in scenes:
        if not isinstance(scene, dict):
            continue
        try:
            scene_id = int(scene.get("scene_id"))
        except Exception:
            continue
        result[scene_id] = scene
    return result


def first_prompt_line(prompt: str | None) -> str:
    if not prompt:
        return ""
    for line in str(prompt).splitlines():
        stripped = line.strip()
        if stripped:
            if stripped.startswith("[") and stripped.endswith("]"):
                continue
            return stripped
    return ""


def build_script_document(*, topic: str, story_scene_map: dict[int, dict], manifest_data: dict) -> str:
    scenes = manifest_data.get("scenes") or []
    script_data: dict = {
        "script_metadata": {
            "topic": topic,
            "source_of_truth": "script.md",
            "derived_from_story": "story.md",
            "derived_from_manifest": "video_manifest.md",
            "consistency_rule": "narration と visual beat は同じ cut の出来事を述べる。manifest は script の実行指示に留める",
        },
        "scenes": [],
    }

    for scene in scenes:
        if not isinstance(scene, dict):
            continue
        if str(scene.get("kind") or "").strip() == "character_reference":
            continue
        try:
            scene_id = int(scene.get("scene_id"))
        except Exception:
            continue

        story_scene = story_scene_map.get(scene_id, {})
        summary = str(story_scene.get("narration") or "").strip()
        visual = str(story_scene.get("visual") or "").strip()
        phase = str(story_scene.get("phase") or "").strip()
        scene_entry: dict = {
            "scene_id": scene_id,
            "phase": phase,
            "scene_summary": summary,
            "story_visual": visual,
            "cuts": [],
        }

        cuts = scene.get("cuts")
        if isinstance(cuts, list) and cuts:
            for cut in cuts:
                if not isinstance(cut, dict):
                    continue
                try:
                    cut_id = int(cut.get("cut_id"))
                except Exception:
                    continue
                image_generation = cut.get("image_generation") or {}
                audio = cut.get("audio") or {}
                narration = (audio.get("narration") if isinstance(audio, dict) else {}) or {}
                scene_entry["cuts"].append(
                    {
                        "cut_id": cut_id,
                        "narration": str(narration.get("text") or "").strip(),
                        "visual_beat": first_prompt_line(str(image_generation.get("prompt") or "")),
                        "image_output": str(image_generation.get("output") or "").strip(),
                    }
                )
        else:
            image_generation = scene.get("image_generation") or {}
            audio = scene.get("audio") or {}
            narration = (audio.get("narration") if isinstance(audio, dict) else {}) or {}
            scene_entry["cuts"].append(
                {
                    "cut_id": 1,
                    "narration": str(narration.get("text") or "").strip(),
                    "visual_beat": first_prompt_line(str(image_generation.get("prompt") or "")),
                    "image_output": str(image_generation.get("output") or "").strip(),
                }
            )
        script_data["scenes"].append(scene_entry)

    return "# 台本（没入型 / canonical）\n\n```yaml\n" + yaml.safe_dump(script_data, sort_keys=False, allow_unicode=True) + "```\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build immersive script.md from story.md + video_manifest.md")
    parser.add_argument("--run-dir", required=True, help="Run directory containing story.md, video_manifest.md, script.md")
    parser.add_argument("--force", action="store_true", help="Overwrite existing script.md")
    args = parser.parse_args()

    if yaml is None:
        raise SystemExit("PyYAML is required. Install with: pip install pyyaml")

    run_dir = Path(args.run_dir).resolve()
    manifest_path = run_dir / "video_manifest.md"
    story_path = run_dir / "story.md"
    script_path = run_dir / "script.md"

    if not manifest_path.exists():
        raise SystemExit(f"Manifest not found: {manifest_path}")
    if script_path.exists() and not args.force:
        raise SystemExit(f"script.md already exists: {script_path} (use --force)")

    manifest_text = manifest_path.read_text(encoding="utf-8")
    manifest_data = yaml.safe_load(extract_yaml_block(manifest_text))
    if not isinstance(manifest_data, dict):
        raise SystemExit("Manifest YAML root must be a mapping.")

    video_metadata = manifest_data.get("video_metadata") or {}
    topic = str(video_metadata.get("topic") or run_dir.name)
    story_scene_map = load_story_scene_map(story_path)

    script_text = build_script_document(topic=topic, story_scene_map=story_scene_map, manifest_data=manifest_data)
    script_path.write_text(script_text, encoding="utf-8")
    print(f"Wrote: {script_path}")


if __name__ == "__main__":
    main()
