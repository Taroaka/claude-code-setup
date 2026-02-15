#!/usr/bin/env python3
"""
State file helper for ToC runs.

State format:
- Append-only key=value blocks separated by a line containing only "---".
- For backward compatibility, we interpret the "current state" as a merge of all keys
  in order (last write wins), even if older blocks were partial updates.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path


def now_iso() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def new_job_id(now: dt.datetime | None = None) -> str:
    n = now or dt.datetime.now()
    return f"JOB_{n.strftime('%Y-%m-%d')}_{n.strftime('%H%M%S')}"


def extract_yaml_block(text: str) -> str:
    m = re.search(r"```yaml\s*\n(.*?)\n```", text, flags=re.DOTALL)
    if not m:
        raise SystemExit("No ```yaml ... ``` block found in manifest markdown.")
    return m.group(1)


def _safe_load_yaml(text: str) -> dict:
    try:
        import yaml  # type: ignore
    except Exception:
        return {}
    try:
        data = yaml.safe_load(text)
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def read_manifest_topic(manifest_path: Path) -> str:
    md = manifest_path.read_text(encoding="utf-8")
    y = extract_yaml_block(md)
    data = _safe_load_yaml(y)
    topic = None
    vm = data.get("video_metadata")
    if isinstance(vm, dict):
        topic = vm.get("topic")
    if topic is None:
        # Minimal fallback: find a top-level "topic:" scalar anywhere.
        m = re.search(r'(?m)^\s*topic:\s*("?)(.+?)\1\s*$', y)
        topic = m.group(2).strip() if m else None
    topic_s = str(topic).strip() if topic is not None else ""
    if not topic_s:
        raise SystemExit(f"Failed to read topic from manifest: {manifest_path}")
    return topic_s


def parse_state_file(state_path: Path) -> dict[str, str]:
    if not state_path.exists():
        return {}
    merged: dict[str, str] = {}
    for raw in state_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line == "---" or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().replace("\n", " ")
        if not k:
            continue
        merged[k] = v
    return merged


def _order_keys(state: dict[str, str]) -> list[str]:
    preferred = [
        "timestamp",
        "job_id",
        "topic",
        "status",
        "runtime.stage",
        "runtime.render.status",
        "review.video.status",
        "review.video.at",
        "review.video.note",
        "artifact.video",
        "artifact.video.short.01",
        "artifact.video_manifest",
        "last_error",
    ]
    out: list[str] = [k for k in preferred if k in state]
    out.extend(sorted(k for k in state.keys() if k not in set(preferred)))
    return out


def append_state_snapshot(state_path: Path, updates: dict[str, str]) -> dict[str, str]:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    merged = parse_state_file(state_path)

    if "job_id" not in merged or not merged["job_id"].strip():
        merged["job_id"] = new_job_id()
    if "status" not in merged or not merged["status"].strip():
        merged["status"] = "INIT"

    merged.update({k: v.replace("\n", " ").strip() for k, v in updates.items()})
    merged["timestamp"] = now_iso()

    lines = [f"{k}={merged[k]}" for k in _order_keys(merged)]
    block = "\n".join(lines) + "\n---\n"
    with state_path.open("a", encoding="utf-8") as f:
        f.write(block)
    return merged


def _resolve_artifact_path(run_dir: Path, value: str | None) -> Path | None:
    if not value:
        return None
    p = Path(value)
    return p if p.is_absolute() else (run_dir / p)


def cmd_ensure(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir)
    manifest = Path(args.manifest)
    state_path = run_dir / "state.txt"

    if state_path.exists():
        return 0

    if not manifest.exists():
        raise SystemExit(f"Manifest not found: {manifest}")

    topic = read_manifest_topic(manifest)
    append_state_snapshot(
        state_path,
        {
            "topic": topic,
            "status": "INIT",
            "runtime.stage": "init",
            "artifact.video_manifest": str(manifest.resolve()),
        },
    )
    return 0


def _parse_set_pairs(pairs: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for raw in pairs:
        if "=" not in raw:
            raise SystemExit(f"Invalid --set (expected key=value): {raw}")
        k, v = raw.split("=", 1)
        k = k.strip()
        v = v.strip()
        if not k:
            raise SystemExit(f"Invalid --set (empty key): {raw}")
        out[k] = v
    return out


def cmd_append(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir)
    state_path = run_dir / "state.txt"
    if not state_path.exists():
        raise SystemExit(f"state.txt not found: {state_path} (run ensure first)")
    updates = _parse_set_pairs(args.set or [])
    if not updates:
        raise SystemExit("--set is required")
    append_state_snapshot(state_path, updates)
    return 0


def cmd_approve_video(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir)
    state_path = run_dir / "state.txt"
    if not state_path.exists():
        raise SystemExit(f"state.txt not found: {state_path} (run ensure first)")
    updates: dict[str, str] = {
        "review.video.status": "approved",
        "review.video.at": now_iso(),
    }
    if args.note:
        updates["review.video.note"] = str(args.note).replace("\n", " ").strip()
    append_state_snapshot(state_path, updates)
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir)
    state_path = run_dir / "state.txt"
    if not state_path.exists():
        raise SystemExit(f"state.txt not found: {state_path}")

    state = parse_state_file(state_path)
    topic = state.get("topic", "")
    stage = state.get("runtime.stage", "")
    render_status = state.get("runtime.render.status", "")
    review_status = state.get("review.video.status", "")
    review_at = state.get("review.video.at", "")
    review_note = state.get("review.video.note", "")
    last_error = state.get("last_error", "")

    artifact_video = _resolve_artifact_path(run_dir, state.get("artifact.video")) or (run_dir / "video.mp4")
    video_exists = artifact_video.exists()

    print(f"Run dir: {run_dir.resolve()}")
    print(f"State: {state_path.resolve()}")
    if topic:
        print(f"Topic: {topic}")
    if stage:
        print(f"Stage: {stage}")
    if render_status:
        print(f"Render: {render_status}")
    print(f"Video: {artifact_video} ({'exists' if video_exists else 'missing'})")
    if review_status:
        s = f"Review: {review_status}"
        if review_at:
            s += f" at {review_at}"
        print(s)
        if review_note:
            print(f"Review note: {review_note}")
    if last_error:
        print(f"Last error: {last_error}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="ToC state.txt helper (append-only snapshots).")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ensure = sub.add_parser("ensure", help="Create state.txt with INIT block if missing.")
    p_ensure.add_argument("--run-dir", required=True)
    p_ensure.add_argument("--manifest", required=True)
    p_ensure.set_defaults(fn=cmd_ensure)

    p_append = sub.add_parser("append", help="Append a state snapshot (merge + updates).")
    p_append.add_argument("--run-dir", required=True)
    p_append.add_argument("--set", action="append", default=[], help="key=value (repeatable)")
    p_append.set_defaults(fn=cmd_append)

    p_approve = sub.add_parser("approve-video", help="Mark video as human-approved.")
    p_approve.add_argument("--run-dir", required=True)
    p_approve.add_argument("--note", default=None)
    p_approve.set_defaults(fn=cmd_approve_video)

    p_show = sub.add_parser("show", help="Show current state summary.")
    p_show.add_argument("--run-dir", required=True)
    p_show.set_defaults(fn=cmd_show)

    args = parser.parse_args()
    return int(args.fn(args))


if __name__ == "__main__":
    raise SystemExit(main())
