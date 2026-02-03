#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


def now_iso() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return ""


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge scene-series scratch notes into a single shared artifact.")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--kind", choices=["research", "story"], required=True)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--out", default=None, help="Override output file (default: research.md or story.md in run dir).")
    parser.add_argument("--force", action="store_true", help="Overwrite output file.")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    scratch_root = run_dir / "scratch"
    if not scratch_root.exists():
        raise SystemExit(f"scratch dir not found: {scratch_root}")

    out_path = Path(args.out).expanduser().resolve() if args.out else (run_dir / ("research.md" if args.kind == "research" else "story.md"))
    if out_path.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite without --force: {out_path}")

    filename = "research_notes.md" if args.kind == "research" else "story_notes.md"
    title = "Research Output" if args.kind == "research" else "Story/Script Notes (Merged)"

    lines: list[str] = []
    lines += [f"# {title}", "", f"- merged_at: {now_iso()}", f"- source: {scratch_root.as_posix()}", ""]

    any_content = False
    for i in range(1, args.workers + 1):
        src = scratch_root / f"ashigaru{i}" / filename
        body = read_text(src)
        body = body.replace("\r\n", "\n").strip()

        if not body:
            continue
        any_content = True

        lines += [f"## Ashigaru {i}", "", f"source: `{src.as_posix()}`", ""]
        lines += [body, ""]

    if not any_content:
        lines += ["(No scratch content found yet.)", ""]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()

