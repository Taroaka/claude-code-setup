#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import subprocess
from pathlib import Path

import yaml


def now_iso() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def tmux_send_two_calls(target: str, message: str) -> None:
    subprocess.run(["tmux", "send-keys", "-t", target, message], check=True)
    subprocess.run(["tmux", "send-keys", "-t", target, "Enter"], check=True)


def load_shogun_command(queue_path: Path) -> dict:
    data = yaml.safe_load(queue_path.read_text(encoding="utf-8")) or {}
    queue = data.get("queue") or []
    if not queue:
        raise SystemExit(f"No commands found in {queue_path}")
    # Use latest entry
    return queue[-1]


def write_task(task_path: Path, task: dict) -> None:
    task_path.parent.mkdir(parents=True, exist_ok=True)
    content = {
        "#": f"足軽{task['task']['assignee']}専用タスクファイル",
        "task": task["task"],
    }
    # Keep format close to existing templates
    lines = ["# " + content["#"]]
    lines += yaml.safe_dump({"task": content["task"]}, sort_keys=False, allow_unicode=True).rstrip().splitlines()
    task_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def research_prompts(worker_count: int) -> list[str]:
    base = [
        "桃太郎の基本あらすじ（要点）を整理し、Q&A動画向けの重要事実を箇条書きにせよ。",
        "登場人物（桃太郎/おじいさん/おばあさん/犬/猿/キジ/鬼）の役割と象徴を整理せよ。",
        "物語の教訓・テーマ（協力/正義/報酬など）を整理し、言い切りの主張候補を作れ。",
        "文化的背景（日本の昔話としての位置づけ・地域差がある点等）を調べ、注意点をまとめよ。",
        "鬼ヶ島・鬼のイメージの扱い（差別/ステレオタイプ回避）観点の注意を書け。",
        "縦動画30-60秒のQ&Aに向く問い（5-10個）を提案せよ（短く答えられるもの）。",
        "視覚化アイデア（図解/抽象/キャラ使い）を提案せよ（テロップ前提で画像内テキスト禁止）。",
        "事実確認の観点で曖昧になりがちな点（地域差/版本差）を洗い出し、断定を避ける表現案を出せ。",
    ]
    if worker_count <= len(base):
        return base[:worker_count]
    return base + [base[-1]] * (worker_count - len(base))


def story_prompts(worker_count: int) -> list[str]:
    base = [
        "scene案を3つ提案（各scene: main_text + question + short answer outline）。",
        "scene案を3つ提案（教育寄り: 教訓/構造）。",
        "scene案を3つ提案（キャラ寄り: 犬猿キジの意味）。",
        "scene案を3つ提案（現代解釈: チームワーク/交渉）。",
        "Q→A→根拠→締め の30-60秒台本テンプレを作れ。",
        "scene間の流れ（seriesとして見た時の順序）を提案せよ。",
        "炎上/誤解回避の言い回しチェック（鬼の扱い含む）を提案せよ。",
        "動画演出の型（フック/結論先出し/リズム）を短く提案せよ。",
    ]
    if worker_count <= len(base):
        return base[:worker_count]
    return base + [base[-1]] * (worker_count - len(base))


def main() -> None:
    parser = argparse.ArgumentParser(description="Dispatch ToC scene-series work to ashigaru via queue/tasks/*.yaml.")
    parser.add_argument("--phase", choices=["research", "story"], required=True)
    parser.add_argument("--queue", default="queue/shogun_to_karo.yaml")
    parser.add_argument("--workers", type=int, default=None, help="Override worker count (default: from command params).")
    parser.add_argument("--wake", action="store_true", help="tmux send-keys to wake each ashigaru pane.")
    args = parser.parse_args()

    queue_path = Path(args.queue).resolve()
    cmd = load_shogun_command(queue_path)
    params = cmd.get("params") or {}

    run_dir = Path(params.get("run_dir") or "").expanduser()
    scratch_root = Path(params.get("scratch_root") or (run_dir / "scratch")).expanduser()
    cmd_id = cmd.get("id") or "cmd"
    worker_count = int(args.workers or params.get("workers") or 8)

    if not run_dir or not run_dir.exists():
        raise SystemExit(f"run_dir not found: {run_dir}")
    scratch_root.mkdir(parents=True, exist_ok=True)

    prompts = research_prompts(worker_count) if args.phase == "research" else story_prompts(worker_count)

    for i in range(1, worker_count + 1):
        scratch_dir = scratch_root / f"ashigaru{i}"
        scratch_dir.mkdir(parents=True, exist_ok=True)

        if args.phase == "research":
            target = scratch_dir / "research_notes.md"
            task_id = f"{cmd_id}_research_{i}"
            desc = f"調査（分担）: {prompts[i-1]} 出力は {target} に追記せよ。共有ファイルは編集禁止。"
        else:
            target = scratch_dir / "story_notes.md"
            task_id = f"{cmd_id}_story_{i}"
            desc = f"台本案（分担）: {prompts[i-1]} 出力は {target} に追記せよ。共有ファイルは編集禁止。"

        task = {
            "task": {
                "task_id": task_id,
                "parent_cmd": cmd_id,
                "description": desc,
                "target_path": str(target),
                "status": "assigned",
                "timestamp": now_iso(),
                "assignee": i,
            }
        }

        task_path = Path("queue/tasks") / f"ashigaru{i}.yaml"
        write_task(task_path, task)

        if args.wake:
            tmux_send_two_calls(
                f"multiagent:0.{i}",
                f"queue/tasks/ashigaru{i}.yaml に任務がある。確認して実行せよ。",
            )

    print(f"Dispatched phase={args.phase} to {worker_count} workers.")
    print(f"Run dir: {run_dir}")
    print(f"Scratch root: {scratch_root}")


if __name__ == "__main__":
    main()

