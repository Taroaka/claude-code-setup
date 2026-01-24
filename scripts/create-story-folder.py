#!/usr/bin/env python3
"""Create a 1-story folder with standard files and subdirs."""
import argparse
import datetime
import os
from pathlib import Path

TEMPLATE_MANIFEST = Path("output/videos/_manifest_template.md")


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str, force: bool):
    if path.exists() and not force:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(description="Create a story folder with standard files.")
    parser.add_argument("--topic", required=True, help="Topic name used in folder name.")
    parser.add_argument("--timestamp", default=None, help="Timestamp (YYYYMMDD_HHMM).")
    parser.add_argument("--base", default="output", help="Base output directory.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")

    args = parser.parse_args()

    ts = args.timestamp
    if not ts:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M")

    folder = Path(args.base) / f"{args.topic}_{ts}"
    ensure_dir(folder)

    # Standard asset subfolders
    assets_dir = folder / "assets"
    ensure_dir(assets_dir / "characters")
    ensure_dir(assets_dir / "styles")
    ensure_dir(assets_dir / "scenes")
    ensure_dir(assets_dir / "audio")

    # Standard empty lists
    write_text(folder / "clips.txt", "", args.force)
    write_text(folder / "narration_list.txt", "", args.force)

    # Placeholders
    write_text(folder / "research.md", "# Research Output\n\nTBD\n", args.force)
    write_text(folder / "story.md", "# Story Script Output\n\nTBD\n", args.force)
    write_text(folder / "script.md", "# Script Output\n\nTBD\n", args.force)
    write_text(folder / "improvement.md", "# Improvement Brief\n\nTBD\n", args.force)

    # Manifest template
    if TEMPLATE_MANIFEST.exists():
        template = TEMPLATE_MANIFEST.read_text(encoding="utf-8")
        template = template.replace("<topic>", args.topic).replace("<timestamp>", ts)
        write_text(folder / "video_manifest.md", template, args.force)
    else:
        write_text(folder / "video_manifest.md", "# Video Manifest\n\nTBD\n", args.force)

    print(f"Created: {folder}")


if __name__ == "__main__":
    main()
