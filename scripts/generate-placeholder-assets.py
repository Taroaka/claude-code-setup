#!/usr/bin/env python3
"""
Generate placeholder assets from a video manifest markdown.

This script is meant to unblock E2E testing before choosing real providers.
It reads the YAML code block inside `video_manifest.md` and creates:
- image_generation.output  (png)
- video_generation.output  (mp4)
- audio.narration.output   (mp3)
"""

from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class SceneAssetSpec:
    scene_id: int
    timestamp: str | None
    image_output: str | None
    video_output: str | None
    narration_output: str | None


def extract_yaml_block(text: str) -> str:
    m = re.search(r"```yaml\s*\n(.*?)\n```", text, flags=re.DOTALL)
    if not m:
        raise SystemExit("No ```yaml ... ``` block found in manifest markdown.")
    return m.group(1)


def parse_timecode(s: str) -> int:
    s = s.strip()
    parts = s.split(":")
    if len(parts) == 2:
        mm, ss = parts
        return int(mm) * 60 + int(ss)
    if len(parts) == 3:
        hh, mm, ss = parts
        return int(hh) * 3600 + int(mm) * 60 + int(ss)
    raise ValueError(f"Unsupported timecode: {s}")


def duration_from_timestamp_range(ts_range: str | None, default_seconds: int) -> int:
    if not ts_range:
        return default_seconds
    raw = ts_range.strip().strip('"').strip("'")
    if "-" not in raw:
        return default_seconds
    start_s, end_s = raw.split("-", 1)
    try:
        start = parse_timecode(start_s)
        end = parse_timecode(end_s)
    except ValueError:
        return default_seconds
    if end <= start:
        return default_seconds
    return end - start


def parse_manifest_yaml(yaml_text: str) -> tuple[tuple[int, int], list[SceneAssetSpec]]:
    resolution = (1080, 1920)
    scenes: list[SceneAssetSpec] = []
    current: SceneAssetSpec | None = None
    stack: list[tuple[int, str]] = []

    def push(indent: int, key: str) -> None:
        nonlocal stack
        while stack and indent <= stack[-1][0]:
            stack.pop()
        stack.append((indent, key))

    for raw in yaml_text.splitlines():
        line = raw.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()

        # list items like "- key: value"
        if stripped.startswith("- "):
            stripped = stripped[2:].strip()

        if ":" not in stripped:
            continue

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()

        push(indent, key)
        context_keys = [k for _, k in stack]

        if key == "resolution" and "video_metadata" in context_keys and value:
            v = value.strip('"').strip("'")
            if "x" in v:
                w_s, h_s = v.split("x", 1)
                try:
                    resolution = (int(w_s), int(h_s))
                except ValueError:
                    pass
            continue

        if key == "scene_id" and "scenes" in context_keys:
            if current:
                scenes.append(current)
            try:
                scene_id = int(value)
            except ValueError:
                scene_id = len(scenes) + 1
            current = SceneAssetSpec(
                scene_id=scene_id,
                timestamp=None,
                image_output=None,
                video_output=None,
                narration_output=None,
            )
            continue

        if not current:
            continue

        if key == "timestamp" and "scenes" in context_keys and value:
            current.timestamp = value.strip('"').strip("'")
            continue

        if key == "output" and value:
            out_path = value.strip('"').strip("'")
            if "image_generation" in context_keys:
                current.image_output = out_path
            elif "video_generation" in context_keys:
                current.video_output = out_path
            elif "narration" in context_keys:
                current.narration_output = out_path

    if current:
        scenes.append(current)

    return resolution, scenes


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def maybe_write_placeholder_image(out_path: Path, width: int, height: int, color: str, force: bool) -> None:
    if out_path.exists() and not force:
        return
    ensure_parent(out_path)
    run(
        [
            "ffmpeg",
            "-hide_banner",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"color=c={color}:s={width}x{height}:d=1",
            "-frames:v",
            "1",
            str(out_path),
        ]
    )


def maybe_write_placeholder_video(out_path: Path, width: int, height: int, duration_seconds: int, color: str, force: bool) -> None:
    if out_path.exists() and not force:
        return
    ensure_parent(out_path)
    run(
        [
            "ffmpeg",
            "-hide_banner",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"color=c={color}:s={width}x{height}:d={duration_seconds}",
            "-r",
            "30",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            str(out_path),
        ]
    )


def maybe_write_placeholder_narration(out_path: Path, duration_seconds: int, force: bool) -> None:
    if out_path.exists() and not force:
        return
    ensure_parent(out_path)
    run(
        [
            "ffmpeg",
            "-hide_banner",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "anullsrc=r=44100:cl=mono",
            "-t",
            str(duration_seconds),
            "-q:a",
            "9",
            "-acodec",
            "libmp3lame",
            str(out_path),
        ]
    )


def color_for_scene(scene_id: int) -> str:
    palette = ["#1f2937", "#0ea5e9", "#22c55e", "#f59e0b", "#ef4444", "#a855f7"]
    return palette[(scene_id - 1) % len(palette)]


def iter_paths(base_dir: Path, *maybe_rel_paths: str | None) -> Iterable[Path]:
    for p in maybe_rel_paths:
        if not p:
            continue
        path = Path(p)
        yield path if path.is_absolute() else (base_dir / path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate placeholder assets for a video manifest.")
    parser.add_argument("--manifest", required=True, help="Path to video_manifest.md (markdown with yaml code block).")
    parser.add_argument(
        "--base-dir",
        default=None,
        help="Base directory to resolve relative asset paths (default: manifest directory).",
    )
    parser.add_argument("--default-scene-seconds", type=int, default=6, help="Fallback seconds if timestamp is missing.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing placeholder files.")

    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        raise SystemExit(f"Manifest not found: {manifest_path}")

    base_dir = Path(args.base_dir) if args.base_dir else manifest_path.parent

    md = manifest_path.read_text(encoding="utf-8")
    yaml_text = extract_yaml_block(md)
    (width, height), scenes = parse_manifest_yaml(yaml_text)

    if not scenes:
        raise SystemExit("No scenes found in manifest YAML.")

    for scene in scenes:
        dur = duration_from_timestamp_range(scene.timestamp, args.default_scene_seconds)
        color = color_for_scene(scene.scene_id)

        for path in iter_paths(base_dir, scene.image_output):
            maybe_write_placeholder_image(path, width, height, color, args.force)

        for path in iter_paths(base_dir, scene.video_output):
            maybe_write_placeholder_video(path, width, height, dur, color, args.force)

        for path in iter_paths(base_dir, scene.narration_output):
            maybe_write_placeholder_narration(path, dur, args.force)

    print(f"Generated placeholders for {len(scenes)} scenes.")


if __name__ == "__main__":
    main()

